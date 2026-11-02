# AI Project Builder Agent

Turn a one-line software idea into a build plan: features, tech stack, folder
structure, database schema, roadmap and starter code.

**How it works**

1. The app asks what you want to build.
2. It acknowledges your idea and asks what the project is for (college project, hackathon, startup MVP, learning / portfolio, or your own answer).
3. The Planner Agent suggests 3 ways to build it, each with the reason you might choose it.
4. You pick one and get the full blueprint, which you can download as Markdown, JSON, or a starter-code ZIP.

**Stack:** Python, FastAPI (backend), Streamlit (frontend), Groq API (LLM), JSON structured output.

```
ai-project-builder-agent/
  backend/
    main.py        FastAPI endpoints: /health, /options, /blueprint
    llm.py         Groq API wrapper that returns parsed JSON
    prompts.py     Prompts and JSON shapes for the Planner Agent
  frontend/
    app.py         Streamlit chat interface
  .streamlit/
    config.toml    Theme colors
  start.py         Starts backend and frontend together
  requirements.txt
  .env.example
```

---

## What to do after downloading the ZIP

### 0. Before you start
- Install **Python 3.10 or newer** (check with `python --version`).
- Get a free **Groq API key** from https://console.groq.com/keys (sign up, then click Create API Key).

### 1. Unzip
Right-click the ZIP and choose **Extract All** (Windows) or double-click it (Mac). You'll get a folder called `ai-project-builder-agent`.

### 2. Open a terminal inside that folder
- **Windows:** open the folder, click the address bar, type `cmd`, press Enter.
- **Mac / Linux:** open Terminal and run `cd path/to/ai-project-builder-agent`.
- **VS Code:** open the folder, then Terminal > New Terminal.

### 3. Create a virtual environment
Windows:
```
python -m venv .venv
.venv\Scripts\activate
```
Mac / Linux:
```
python3 -m venv .venv
source .venv/bin/activate
```
You should now see `(.venv)` at the start of your terminal line.

### 4. Install the dependencies
```
pip install -r requirements.txt
```

### 5. Add your API key
Copy `.env.example` to a new file named `.env`:

Windows: `copy .env.example .env`
Mac / Linux: `cp .env.example .env`

Open `.env` in any text editor and replace `your-api-key-here` with your real key. Save the file.

### 6. Run the app
Easiest way (starts backend and frontend together):
```
python start.py
```

Or, if you prefer two terminals (activate the virtual environment in both):

Terminal 1, backend:
```
uvicorn backend.main:app --port 8000 --reload
```
Terminal 2, frontend:
```
streamlit run frontend/app.py
```

### 7. Open the app
Go to **http://localhost:8501** in your browser if it doesn't open by itself. The sidebar should say "Backend connected". Type your idea and follow the chat.

To stop the app, press `Ctrl + C` in the terminal.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Sidebar says "Backend offline" | The backend isn't running. Use `python start.py`, or start `uvicorn` as shown above. Make sure you run commands from the project folder. |
| "GROQ_API_KEY is missing" | Check that the file is named `.env` (not `.env.example` or `.env.txt`) and that you restarted the app after editing it. |
| "API key was rejected" | The key is wrong or was deleted. Create a new one at https://console.groq.com/keys. |
| "Model ... was not found" | Set `GROQ_MODEL` in `.env` to a model listed at https://console.groq.com/docs/models. |
| `ModuleNotFoundError` | The virtual environment isn't active, or step 4 was skipped. |
| Port already in use | Close the other app using port 8000 or 8501, or run with a different port: `streamlit run frontend/app.py --server.port 8502`. |
| Blueprint takes long | Normal. The full blueprint can take up to a minute. |
| "Groq rate limit reached" | The free tier has per-minute limits. Wait a minute and try again. |

## Settings (`.env`)
- `GROQ_API_KEY`: your key (required)
- `GROQ_MODEL`: model used by the Planner Agent (default `llama-3.3-70b-versatile`)
- `BACKEND_URL`: where the frontend finds the backend (default `http://localhost:8000`)

## Ideas for extending it
GitHub integration, multiple specialized agents, automatic code generation, automated testing, debugging agents, Docker-based execution, one-click deployment.
