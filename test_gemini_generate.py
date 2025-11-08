import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

prompt = """
Summarize this article in two lines:
The Reserve Bank of India raised the repo rate by 25 basis points to control inflation.
"""

try:
    response = model.generate_content(prompt)
    print("\n✅ Gemini Response:\n")
    print(response.text)
except Exception as e:
    print("\n❌ Error:\n", e)
