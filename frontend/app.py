"""Streamlit frontend for the AI Project Builder Agent."""
import html
import io
import json
import os
import re
import zipfile

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Project Builder Agent", page_icon="📐", layout="wide")

# ---------------------------------------------------------------- styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
html, body, .stApp, .stMarkdown, .stButton button, textarea, input {
  font-family: 'IBM Plex Sans', system-ui, sans-serif;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
  font-family: 'Bricolage Grotesque', 'IBM Plex Sans', sans-serif;
  letter-spacing: -0.01em; color: #4C1D95;
}
.block-container { max-width: 1180px; padding-top: 1.4rem; }
.hero {
  background-image:
    radial-gradient(rgba(255,255,255,.22) 1.5px, transparent 1.5px),
    linear-gradient(120deg, #6D28D9 0%, #DB2777 55%, #F97316 100%);
  background-size: 22px 22px, 100% 100%;
  border-radius: 18px; padding: 30px 34px; margin-bottom: 1.2rem;
  box-shadow: 0 10px 30px rgba(124,58,237,.25);
}
.hero .title { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700;
  font-size: 2.4rem; color: #fff; margin: 0 0 6px 0; line-height: 1.15; }
.hero .sub { color: #FFF1F8; font-size: 1.05rem; margin: 0 0 14px 0; max-width: 660px; }
.pills span { display: inline-block; margin: 0 8px 6px 0; padding: 4px 12px; border-radius: 999px;
  background: rgba(255,255,255,.2); border: 1px solid rgba(255,255,255,.45); color: #fff; font-size: .85rem; }
[data-testid="stChatMessage"] { background: #fff; border: 1px solid #EADDFB; border-radius: 14px; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #F3E8FF 0%, #FFE4EF 60%, #FFEDD5 100%); }
.stButton > button, .stDownloadButton > button { width: 100%; border-radius: 12px; font-weight: 600;
  border: 2px solid #C4B5FD; transition: transform .12s ease, box-shadow .12s ease; }
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(124,58,237,.25); border-color: #7C3AED; }
.stButton > button[kind="primary"], .stButton > button[data-testid="stBaseButton-primary"] {
  background: linear-gradient(90deg, #7C3AED, #EC4899); color: #fff; border: none; }
.stButton > button[kind="primary"] p, .stButton > button[data-testid="stBaseButton-primary"] p { color: #fff; }
.stDownloadButton > button { background: linear-gradient(90deg, #0EA5E9, #14B8A6); color: #fff; border: none; }
.stDownloadButton > button p { color: #fff; }
.chip { display: inline-block; padding: 2px 11px; margin: 0 6px 6px 0; border-radius: 999px;
  background: #F3F4F6; color: #374151; font-size: .82rem; font-weight: 500; }
.chip.c0 { background: #EDE9FE; color: #5B21B6; }
.chip.c1 { background: #FCE7F3; color: #9D174D; }
.chip.c2 { background: #FFEDD5; color: #9A3412; }
.chip.c3 { background: #CCFBF1; color: #115E59; }
.chip.c4 { background: #E0F2FE; color: #075985; }
.chip.c5 { background: #DCFCE7; color: #166534; }
.chip.must { background: linear-gradient(90deg, #7C3AED, #EC4899); color: #fff; }
.chip.should { background: #FEF3C7; color: #92400E; }
.chip.nice { background: #CCFBF1; color: #115E59; }
.bar { height: 6px; border-radius: 999px; margin-bottom: 12px; }
.b0 { background: linear-gradient(90deg, #7C3AED, #EC4899); }
.b1 { background: linear-gradient(90deg, #F97316, #F59E0B); }
.b2 { background: linear-gradient(90deg, #14B8A6, #0EA5E9); }
.b3 { background: linear-gradient(90deg, #EC4899, #F97316); }
.b4 { background: linear-gradient(90deg, #0EA5E9, #7C3AED); }
.b5 { background: linear-gradient(90deg, #22C55E, #14B8A6); }
.steps { padding: 0; margin: 0; }
.steps li { list-style: none; padding: 9px 12px; margin-bottom: 8px; border-radius: 10px;
  border-left: 5px solid #E9D5FF; color: #7C6A9B; background: rgba(255,255,255,.45); }
.steps li.done { border-left-color: #14B8A6; color: #115E59; background: rgba(255,255,255,.75); }
.steps li.now { border-left-color: #EC4899; background: #fff; color: #4C1D95; font-weight: 600;
  box-shadow: 0 4px 12px rgba(236,72,153,.18); }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- helpers
PURPOSES = [
    ("College project", "Semester, mini or final-year project"),
    ("Hackathon", "Build a working demo in a day or two"),
    ("Startup MVP", "Validate an idea with real users"),
    ("Learning / portfolio", "Practice skills and show your work"),
]
STEPS = ["Describe your idea", "Pick the purpose", "Compare options", "Get your blueprint"]
STAGE_TO_STEP = {"idea": 0, "purpose": 1, "options_loading": 2, "options": 2,
                 "blueprint_loading": 3, "blueprint": 3}
AVATARS = {"assistant": "📐", "user": "🧑‍💻"}


class ApiError(Exception):
    pass


def call_api(path: str, payload: dict) -> dict:
    try:
        r = requests.post(f"{BACKEND_URL}{path}", json=payload, timeout=240)
    except requests.exceptions.ConnectionError:
        raise ApiError(
            f"Can't reach the backend at {BACKEND_URL}. Start it with: "
            "uvicorn backend.main:app --port 8000"
        )
    except requests.exceptions.Timeout:
        raise ApiError("The request took too long. Please try again.")
    if r.status_code != 200:
        try:
            detail = r.json().get("detail", r.text)
        except ValueError:
            detail = r.text
        raise ApiError(str(detail))
    return r.json()


@st.cache_data(ttl=10)
def backend_ok() -> bool:
    try:
        return requests.get(f"{BACKEND_URL}/health", timeout=2).status_code == 200
    except requests.exceptions.RequestException:
        return False


def chips(items, cls=""):
    items = [i for i in items if i]
    return "".join(
        f'<span class="chip {cls or "c" + str(n % 6)}">{html.escape(str(i))}</span>'
        for n, i in enumerate(items)
    )


def add_msg(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})


def init_state():
    if "stage" not in st.session_state:
        st.session_state.update(
            stage="idea", idea="", purpose="", options=[], chosen=None, blueprint=None,
            messages=[{"role": "assistant",
                       "content": "Hi! What do you want to build? Describe it in a sentence or two."}],
        )


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-") or "project"


def safe_path(path: str):
    parts = [p for p in str(path).replace("\\", "/").split("/") if p not in ("", ".")]
    if not parts or ".." in parts:
        return None
    return "/".join(parts)


def blueprint_markdown(bp: dict) -> str:
    g = bp.get
    out = [f"# {g('project_name', 'Project Blueprint')}", "", g("one_line_summary", ""), "", "## Features"]
    for f in g("features", []):
        out.append(f"- **{f.get('name', '')}** ({f.get('priority', '')}): {f.get('description', '')}")
    out += ["", "## Non-functional requirements"] + [f"- {x}" for x in g("non_functional_requirements", [])]
    out += ["", "## Tech stack"]
    for t in g("tech_stack", []):
        out.append(f"- **{t.get('layer', '')}**: {t.get('choice', '')}. {t.get('reason', '')}")
    out += ["", "## Folder structure", "```", g("folder_structure", ""), "```", "", "## Database schema"]
    for t in g("database_schema", []):
        out += [f"### {t.get('table', '')}", t.get("purpose", ""), "",
                "| Column | Type | Notes |", "|---|---|---|"]
        out += [f"| {c.get('name', '')} | {c.get('type', '')} | {c.get('notes', '')} |"
                for c in t.get("columns", [])]
        out.append("")
    out.append("## Roadmap")
    for i, p in enumerate(g("roadmap", []), 1):
        out += [f"### Phase {i}: {p.get('phase', '')} ({p.get('duration', '')})", p.get("goal", "")]
        out += [f"- {t}" for t in p.get("tasks", [])]
        out.append("")
    out.append("## Starter code")
    for f in g("starter_code", []):
        out += [f"### {f.get('path', '')}", f.get("description", ""),
                f"```{f.get('language', '')}", f.get("code", ""), "```", ""]
    return "\n".join(out)


def starter_zip(bp: dict) -> bytes:
    root = slug(bp.get("project_name", "project"))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{root}/BLUEPRINT.md", blueprint_markdown(bp))
        for f in bp.get("starter_code", []):
            p = safe_path(f.get("path", ""))
            if p:
                z.writestr(f"{root}/{p}", f.get("code", ""))
    return buf.getvalue()


# ---------------------------------------------------------------- state
init_state()
ss = st.session_state

def choose_purpose(purpose: str):
    ss.purpose = purpose
    add_msg("user", f"It's for: {purpose}")
    add_msg("assistant", f"Thanks. I'll look for a few ways to build this as a **{purpose.lower()}**.")
    ss.stage = "options_loading"
    st.rerun()


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown("### Progress")
    now = STAGE_TO_STEP[ss.stage]
    items = "".join(
        f'<li class="{"now" if i == now else "done" if i < now else ""}">{html.escape(label)}</li>'
        for i, label in enumerate(STEPS)
    )
    st.markdown(f'<ul class="steps">{items}</ul>', unsafe_allow_html=True)
    if st.button("Start over"):
        st.session_state.clear()
        st.rerun()
    st.markdown("---")
    if backend_ok():
        st.success("Backend connected")
    else:
        st.error("Backend offline. Start it, then refresh this page.")

# ---------------------------------------------------------------- header
st.markdown(
    '<div class="hero"><p class="title">AI Project Builder Agent</p>'
    '<p class="sub">Describe an idea. Get requirements, a tech stack, folder structure, '
    "database schema, roadmap and starter code you can start building today.</p>"
    '<div class="pills"><span>Requirements</span><span>Tech stack</span><span>Folder structure</span>'
    '<span>Database</span><span>Roadmap</span><span>Starter code</span></div></div>',
    unsafe_allow_html=True,
)

for m in ss.messages:
    with st.chat_message(m["role"], avatar=AVATARS[m["role"]]):
        st.markdown(m["content"])

err = ss.pop("error", None)
if err:
    st.error(err)

# ---------------------------------------------------------------- stages
if ss.stage == "idea":
    idea = st.chat_input("Example: a website where students can find study partners")
    if idea and idea.strip():
        ss.idea = idea.strip()
        add_msg("user", ss.idea)
        add_msg("assistant",
                f"Got it. **{ss.idea}** is a good one to build.\n\n"
                "What is this project for? Pick one below, or type your own answer in the box.")
        ss.stage = "purpose"
        st.rerun()

elif ss.stage == "purpose":
    cols = st.columns(len(PURPOSES))
    for col, (label, hint) in zip(cols, PURPOSES):
        if col.button(label, help=hint, key=f"purpose_{label}"):
            choose_purpose(label)
    typed = st.chat_input('Or type something else, like "final-year capstone" or "client demo"')
    if typed and typed.strip():
        choose_purpose(typed.strip())

elif ss.stage == "options_loading":
    with st.spinner("Comparing ways to build your project..."):
        try:
            data = call_api("/options", {"idea": ss.idea, "purpose": ss.purpose})
            opts = data.get("options", [])[:3]
            if not opts:
                raise ApiError("No options came back. Please try again.")
            ss.options = opts
            add_msg("assistant",
                    f"Here are {len(opts)} ways to build it for a **{ss.purpose.lower()}**. "
                    "Pick the one that fits you best.")
            ss.stage = "options"
        except ApiError as e:
            ss.error = str(e)
            ss.stage = "purpose"
    st.rerun()

elif ss.stage == "options":
    cols = st.columns(len(ss.options))
    for idx, (col, opt) in enumerate(zip(cols, ss.options)):
        with col, st.container(border=True):
            st.markdown(f'<div class="bar b{idx % 6}"></div>', unsafe_allow_html=True)
            st.markdown(f"#### {opt.get('title', 'Option')}")
            st.caption(opt.get("tagline", ""))
            st.markdown(chips([opt.get("difficulty"), opt.get("estimated_time")]), unsafe_allow_html=True)
            st.markdown("**Why pick this**")
            st.write(opt.get("why_choose", ""))
            st.markdown(f"**Best for:** {opt.get('best_for', '')}")
            st.markdown("**Suggested stack**")
            st.markdown(chips(opt.get("suggested_stack", [])), unsafe_allow_html=True)
            st.markdown("**Key features**")
            st.markdown("\n".join(f"- {f}" for f in opt.get("key_features", [])))
            if st.button("Build this one", type="primary", key=f"pick_{opt.get('id', opt.get('title'))}"):
                ss.chosen = opt
                add_msg("user", f"I'll go with **{opt.get('title', 'this option')}**.")
                add_msg("assistant",
                        "Good choice. I'm writing your blueprint now: features, stack, folders, "
                        "database, roadmap and starter code. This can take up to a minute.")
                ss.stage = "blueprint_loading"
                st.rerun()

elif ss.stage == "blueprint_loading":
    with st.spinner("Writing your project blueprint..."):
        try:
            ss.blueprint = call_api(
                "/blueprint", {"idea": ss.idea, "purpose": ss.purpose, "option": ss.chosen}
            )
            add_msg("assistant", "Your blueprint is ready. Explore the tabs below, then download it.")
            ss.stage = "blueprint"
        except ApiError as e:
            ss.error = str(e)
            ss.stage = "options"
    st.rerun()

elif ss.stage == "blueprint":
    bp = ss.blueprint or {}
    st.markdown(f"## {bp.get('project_name', 'Your project')}")
    st.write(bp.get("one_line_summary", ""))

    d1, d2, d3 = st.columns(3)
    name = slug(bp.get("project_name", "project"))
    d1.download_button("Download blueprint (.md)", blueprint_markdown(bp), f"{name}-blueprint.md", "text/markdown")
    d2.download_button("Download starter code (.zip)", starter_zip(bp), f"{name}-starter.zip", "application/zip")
    d3.download_button("Download raw JSON", json.dumps(bp, indent=2), f"{name}.json", "application/json")

    tabs = st.tabs(["Overview", "Tech stack", "Folder structure", "Database", "Roadmap", "Starter code"])

    with tabs[0]:
        st.markdown("#### Features")
        order = {"must": 0, "should": 1, "nice": 2}
        feats = sorted(bp.get("features", []), key=lambda f: order.get(str(f.get("priority", "")).lower(), 3))
        for f in feats:
            pr = str(f.get("priority", ""))
            st.markdown(
                f'{chips([pr], pr.lower())} **{html.escape(str(f.get("name", "")))}**  \n'
                f'{html.escape(str(f.get("description", "")))}',
                unsafe_allow_html=True,
            )
        st.markdown("#### Non-functional requirements")
        st.markdown("\n".join(f"- {x}" for x in bp.get("non_functional_requirements", [])))

    with tabs[1]:
        rows = [{"Layer": t.get("layer", ""), "Choice": t.get("choice", ""), "Why": t.get("reason", "")}
                for t in bp.get("tech_stack", [])]
        if rows:
            st.table(rows)

    with tabs[2]:
        st.code(bp.get("folder_structure", ""), language=None)

    with tabs[3]:
        tables = bp.get("database_schema", [])
        if not tables:
            st.info("This project doesn't need a database for its first version.")
        for t in tables:
            st.markdown(f"#### {t.get('table', '')}")
            st.caption(t.get("purpose", ""))
            st.table([{"Column": c.get("name", ""), "Type": c.get("type", ""), "Notes": c.get("notes", "")}
                      for c in t.get("columns", [])])

    with tabs[4]:
        for i, p in enumerate(bp.get("roadmap", []), 1):
            with st.container(border=True):
                st.markdown(f'<div class="bar b{(i - 1) % 6}"></div>', unsafe_allow_html=True)
                st.markdown(f"#### Phase {i}: {p.get('phase', '')}")
                st.caption(f"{p.get('duration', '')}  |  Goal: {p.get('goal', '')}")
                st.markdown("\n".join(f"- {t}" for t in p.get("tasks", [])))

    with tabs[5]:
        for i, f in enumerate(bp.get("starter_code", [])):
            with st.expander(f"{f.get('path', '')}", expanded=(i == 0)):
                st.caption(f.get("description", ""))
                st.code(f.get("code", ""), language=f.get("language") or None)
