# Model-regression-detection-system

## Setup

1. Get a free Groq API key (no credit card): https://console.groq.com
2. Create a `.env` file in the project root:
   ```
   GROQ_API_KEY="your-key-here"
   LLM_BASE_URL="https://api.groq.com/openai/v1"
   LLM_MODEL="llama-3.3-70b-versatile"
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Run the eval suite: `python -m src.eval_runner`