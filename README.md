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
4. Run the eval suite (loads `.env` automatically via `python-dotenv`):
   - `python -m src.eval_runner`
   - If you want to load a specific env file: `python -c "from dotenv import load_dotenv; load_dotenv('path/to/.env'); import runpy; runpy.run_module('src.eval_runner', run_name='__main__')"`

