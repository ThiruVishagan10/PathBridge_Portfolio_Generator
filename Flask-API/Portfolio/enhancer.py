import os
import time
import random
from dotenv import load_dotenv
import google.generativeai as genai

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

# Initialize the model once
try:
    model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    model = None


def enhance_content(prompt_instruction: str, content: str, retries: int = 3) -> str:
    """
    Enhances a single piece of content using Gemini API with retry logic.
    """
    # Temporarily disabled for faster generation
    return content if content else ""


def enhance_batch(prompt_instruction: str, items: list[str], retries: int = 3) -> list[str]:
    """
    Enhances a list of items in one API call to save credits.
    
    Args:
        prompt_instruction (str): General instruction for rewriting the items.
        items (list[str]): List of strings to enhance.
        retries (int): Number of retry attempts.

    Returns:
        list[str]: Enhanced items, maintaining order.
    """
    # Temporarily disabled for faster generation
    return items if items else []
