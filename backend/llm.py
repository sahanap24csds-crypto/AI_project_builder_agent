"""Thin wrapper around the Groq API that always returns parsed JSON."""
import json
import os
import re

import groq
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


class LLMError(Exception):
    """Raised for problems the user can fix (missing key, bad model output)."""


def _client() -> Groq:
    key = os.getenv("GROQ_API_KEY", "").strip()
    if not key or key == "your-api-key-here":
        raise LLMError(
            "GROQ_API_KEY is missing. Add it to your .env file and restart the backend."
        )
    return Groq(api_key=key, timeout=120.0)


def _parse_json(text: str):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            return json.loads(text[start : end + 1])
        raise


def ask_json(system: str, user: str, max_tokens: int = 4000) -> dict:
    client = _client()
    for _ in range(2):  # one retry if the model returns broken JSON
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                response_format={"type": "json_object"},
                temperature=0.4,
                max_tokens=max_tokens,
            )
        except groq.BadRequestError as e:
            if "json_validate_failed" in str(e):
                continue
            raise
        text = resp.choices[0].message.content or ""
        try:
            return _parse_json(text)
        except json.JSONDecodeError:
            continue
    raise LLMError("The model returned an invalid response. Please try again.")
