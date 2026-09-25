"""
Utility functions for the HTA GenAI consistency project.
Uses Google Gemini API (free tier) with retry and backoff logic.
"""

import os
import json
import re
import time
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

import google.generativeai as genai

# --- Configure Gemini ---
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-3.6-flash"   # fast and free-tier friendly
# Alternative: "gemini-1.5-pro" (slower, higher quality, lower free quota)


def call_llm(prompt: str, temperature: float = 0.0,
             max_retries: int = 5, base_delay: float = 5.0) -> str:
    """
    Send a prompt to Gemini and return the raw text response.
    Retries on rate-limit and transient errors with exponential backoff.
    """
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set. Check your .env file.")

    model = genai.GenerativeModel(MODEL_NAME)

    last_error = None
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": 2000,
                }
            )
            # Gemini sometimes returns no text if blocked
            if not response.text:
                raise ValueError("Empty response from Gemini (possibly blocked).")
            return response.text

        except Exception as e:
            last_error = e
            msg = str(e).lower()

            # Detect rate-limit / quota errors and back off
            if "quota" in msg or "rate" in msg or "429" in msg:
                delay = base_delay * (2 ** attempt)
                print(f"  [rate limit] waiting {delay:.0f}s "
                      f"(attempt {attempt+1}/{max_retries})...")
                time.sleep(delay)
            else:
                # Other errors: shorter wait, still retry
                delay = base_delay
                print(f"  [error] {e} — retrying in {delay:.0f}s "
                      f"(attempt {attempt+1}/{max_retries})...")
                time.sleep(delay)

    raise RuntimeError(f"LLM call failed after {max_retries} attempts: {last_error}")


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """Extract a JSON object from an LLM response."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_json(data: Any, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(value: str) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def values_match(a: str, b: str, threshold: float = 0.3) -> bool:
    """Lower threshold and check for key numbers."""
    import re

    na, nb = normalize(a), normalize(b)
    if not na or not nb:
        return na == nb
    if na == "not found" or nb == "not found":
        return na == nb

    # Extract numbers from both
    nums_a = set(re.findall(r"\d+\.?\d*", na))
    nums_b = set(re.findall(r"\d+\.?\d*", nb))

    if nums_a and nums_b:
        # If key numbers overlap, consider it a match
        overlap = nums_a & nums_b
        if len(overlap) / max(len(nums_b), 1) >= 0.5:
            return True

    # Fall back to token overlap with lower threshold
    tokens_a = set(na.replace(",", " ").replace("(", " ").replace(")", " ").split())
    tokens_b = set(nb.replace(",", " ").replace("(", " ").replace(")", " ").split())
    if not tokens_a or not tokens_b:
        return False
    overlap = tokens_a & tokens_b
    return len(overlap) / max(len(tokens_b), 1) >= threshold