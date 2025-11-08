import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Configure Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file!")
    exit()

genai.configure(api_key=api_key)

try:
    print("🔍 Checking available Gemini models...\n")
    models = [m.name for m in genai.list_models()]
    for model in models:
        print("✅", model)
    print("\n🎯 Gemini API connection successful!")

except Exception as e:
    print("❌ Error connecting to Gemini API:\n", e)
