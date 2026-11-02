"""Starts the FastAPI backend and the Streamlit frontend together.

Usage:  python start.py
Stop both with Ctrl+C.
"""
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    procs = [
        subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.main:app", "--port", "8000"],
            cwd=ROOT,
        ),
        subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "frontend/app.py"],
            cwd=ROOT,
        ),
    ]
    try:
        while all(p.poll() is None for p in procs):
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        for p in procs:
            if p.poll() is None:
                p.terminate()


if __name__ == "__main__":
    main()
