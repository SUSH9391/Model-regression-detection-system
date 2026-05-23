# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runner
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy user-site package installs from the builder stage
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy source code and configurations
COPY src/ /app/src/
COPY data/ /app/data/
COPY prompts/ /app/prompts/

# Ensure reports directory exists
RUN mkdir -p /app/reports

# Environment variables placeholders (no hardcoded keys)
ENV OPENAI_API_KEY=""
ENV SLACK_WEBHOOK_URL=""

# Default execution command runs evaluation runner
CMD ["python", "-m", "src.eval_runner"]
