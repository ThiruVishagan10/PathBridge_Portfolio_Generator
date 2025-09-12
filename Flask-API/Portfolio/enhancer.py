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
    if not content or not content.strip():
        return ""

    full_prompt = (
        f"{prompt_instruction}\n\n"
        f"Content: {content}\n\n"
        f"Return ONLY the improved result. Do not include explanations, notes, or extra text."
    )

    for attempt in range(retries):
        try:
            if not model:
                return content

            response = model.generate_content(full_prompt)
            if response and hasattr(response, "text") and response.text:
                result = response.text.strip()
                for line in result.split("\n"):
                    if line.strip():
                        return line.strip()
            return content
        except Exception as e:
            print(f"Enhancement attempt {attempt+1} failed: {e}")
            time.sleep((2 ** attempt) + random.random())

    return content


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
    if not items:
        return []

    # Build prompt with numbered list
    items_text = "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])
    full_prompt = (
        f"{prompt_instruction}\n\n"
        f"Here is a list of items:\n{items_text}\n\n"
        f"Return ONLY the improved items as a numbered list, same order, no explanations."
    )

    for attempt in range(retries):
        try:
            if not model:
                return items

            response = model.generate_content(full_prompt)
            if response and hasattr(response, "text") and response.text:
                result = response.text.strip()
                enhanced = []
                for line in result.split("\n"):
                    line = line.strip()
                    if line and any(ch.isalnum() for ch in line):
                        # Remove leading numbering like "1. " or "- "
                        cleaned = line.lstrip("0123456789.-) ").strip()
                        enhanced.append(cleaned)
                return enhanced if enhanced else items
            return items
        except Exception as e:
            print(f"Batch enhancement attempt {attempt+1} failed: {e}")
            time.sleep((2 ** attempt) + random.random())

    return items
