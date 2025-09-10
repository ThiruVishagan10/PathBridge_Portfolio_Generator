import os
import google.generativeai as genai
import time
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Google Generative AI client
try:
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=API_KEY)
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

# Initialize the model once for efficiency
model = genai.GenerativeModel("gemini-1.5-pro")

def enhance_content(prompt_instruction: str, content: str) -> str:
    """
    Enhances content using Gemini API.
    """
    if not content.strip():
        return ""
    
    try:
        full_prompt = f"{prompt_instruction}\n\nContent: {content}\n\nReturn ONLY the result, no explanations:"
        response = model.generate_content(full_prompt)
        result = response.text.strip() if response and response.text else content
        # Return only first line to avoid verbose responses
        return result.split('\n')[0].strip() if result else content
    except Exception as e:
        print(f"Enhancement failed: {e}")
        return content
