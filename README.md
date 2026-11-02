# 🤖 AI Project Builder Agent

**Turn a one-line software idea into a complete project blueprint using AI.**

AI Project Builder Agent transforms simple project ideas into structured development plans, including features, technology stack, folder structure, database schema, development roadmap, and starter code.

Instead of spending hours planning a project from scratch, describe your idea and let the AI Planner Agent guide you through the development process.

## ✨ Key Features

- **Idea Understanding:** Converts simple project descriptions into structured project concepts.
- **Purpose-Based Planning:** Supports college projects, hackathons, startup MVPs, and learning/portfolio projects.
- **Multiple Approaches:** Suggests three different ways to build a project, with reasons for choosing each approach.
- **Smart Tech Stack Selection:** Recommends suitable technologies based on project requirements.
- **Project Architecture:** Generates folder structures and database schemas.
- **Development Roadmap:** Breaks the project into manageable development tasks.
- **Starter Code Generation:** Provides downloadable starter code to kick-start development.
- **Multiple Export Options:** Download the generated blueprint in Markdown, JSON, or ZIP format.

## ⚙️ How It Works

1. **Describe Your Idea:** Enter your software project idea in a sentence or two.
2. **Select the Purpose:** Choose whether it is a college project, hackathon, startup MVP, learning/portfolio project, or another purpose.
3. **Explore Approaches:** The Planner Agent suggests three possible development approaches and explains their advantages.
4. **Choose an Approach:** Select the approach that best matches your requirements.
5. **Generate Your Blueprint:** Receive a complete project plan containing requirements, tech stack, folder structure, database schema, roadmap, and starter code.
6. **Download and Build:** Export your blueprint as Markdown, JSON, or a starter-code ZIP.


## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | Streamlit |
| AI / LLM | Groq API |
| AI Model | Llama 3.3 70B Versatile (default) |
| Data Format | JSON Structured Output |
| Configuration | Python dotenv |


## 🚀 Getting Started

Follow these steps to run the project locally.

### 1. Prerequisites

- Python 3.10 or newer
- Git
- A free Groq API key

Get your API key from: [Groq Console](https://console.groq.com/keys)

### 2. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project folder:

```bash
cd AI-Project-Builder-Agent
```

### 3. Create a Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Alternatively, in Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

**Mac / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file by copying `.env.example`.

**Windows:**

```powershell
Copy-Item .env.example .env
```

**Mac / Linux:**

```bash
cp .env.example .env
```

Open `.env` and add your Groq API key:

```env
GROQ_API_KEY=your-api-key-here
GROQ_MODEL=llama-3.3-70b-versatile
BACKEND_URL=http://localhost:8000
```

**Important:** Never upload your actual `.env` file or API key to GitHub.

### 6. Run the Application

Start both the backend and frontend together:

```bash
python start.py
```

Alternatively, start them separately in two terminals.

**Terminal 1 – Backend:**

```bash
uvicorn backend.main:app --port 8000 --reload
```

**Terminal 2 – Frontend:**

```bash
streamlit run frontend/app.py
```

### 7. Access the Application

Open your browser and visit:

**http://localhost:8501**

The sidebar should display **Backend connected**.

Enter your project idea and follow the AI-guided workflow to generate your project blueprint.

To stop the application, press `Ctrl + C` in the terminal.

## 🔐 Environment Variables

| Variable | Description | Default |
|---|---|---|
| `GROQ_API_KEY` | Groq API authentication key | Required |
| `GROQ_MODEL` | LLM model used by the Planner Agent | `llama-3.3-70b-versatile` |
| `BACKEND_URL` | Backend API address | `http://localhost:8000` |

## 🐛 Troubleshooting

| Issue | Possible Solution |
|---|---|
| Backend offline | Make sure the backend is running using `python start.py`. |
| GROQ_API_KEY is missing | Check that your `.env` file exists and contains the API key. |
| API key rejected | Generate a new API key from the Groq Console. |
| Model not found | Check the available models in the [Groq documentation](https://console.groq.com/docs/models). |
| ModuleNotFoundError | Activate the virtual environment and install dependencies again. |
| Port already in use | Close the process using port 8000 or 8501, or configure another port. |
| Blueprint takes time | Allow some time for the LLM to generate the complete blueprint. |
| Groq rate limit reached | Wait and retry after the API rate limit resets. |

## 🔮 Future Enhancements

- GitHub integration for directly creating project repositories.
- Multiple specialized AI agents for different development tasks.
- Advanced automatic code generation.
- Automated code testing and debugging.
- Docker-based project execution.
- One-click project deployment.

## 💡 Why This Project?

Starting a software project often involves multiple challenges, from selecting the right technology stack to designing the architecture and planning development tasks.

AI Project Builder Agent simplifies this process by transforming an initial idea into an actionable development blueprint.

**The goal is simple: Spend less time planning and more time building.**

---

**Built with Python, FastAPI, Streamlit, and Groq AI.**
