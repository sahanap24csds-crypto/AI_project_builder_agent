"""FastAPI backend: receives the idea and asks the Planner Agent for results."""
import groq
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.llm import MODEL, LLMError, ask_json
from backend.prompts import SYSTEM, blueprint_prompt, options_prompt

app = FastAPI(title="AI Project Builder Agent")


class OptionsRequest(BaseModel):
    idea: str = Field(min_length=3, max_length=2000)
    purpose: str = Field(min_length=2, max_length=300)


class BlueprintRequest(OptionsRequest):
    option: dict


def _run(fn):
    try:
        return fn()
    except LLMError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except groq.AuthenticationError:
        raise HTTPException(status_code=401, detail="The Groq API key was rejected. Check your .env file.")
    except groq.RateLimitError:
        raise HTTPException(status_code=429, detail="Groq rate limit reached. Wait a minute and try again.")
    except groq.NotFoundError:
        raise HTTPException(status_code=400, detail=f"Model '{MODEL}' was not found. Change GROQ_MODEL in .env.")
    except groq.BadRequestError as e:
        raise HTTPException(status_code=400, detail=f"Groq rejected the request (check GROQ_MODEL in .env): {e}")
    except groq.APIConnectionError:
        raise HTTPException(status_code=502, detail="Could not reach the Groq API. Check your internet connection.")
    except Exception as e:  # keep the UI alive with a readable message
        raise HTTPException(status_code=502, detail=f"Planner Agent failed: {e}")


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL}


@app.post("/options")
def options(req: OptionsRequest):
    return _run(lambda: ask_json(SYSTEM, options_prompt(req.idea, req.purpose), max_tokens=3000))


@app.post("/blueprint")
def blueprint(req: BlueprintRequest):
    return _run(
        lambda: ask_json(SYSTEM, blueprint_prompt(req.idea, req.purpose, req.option), max_tokens=6000)
    )
