"""
Application entry point (Lab 3).
Run locally:  python main.py
Docker:       CMD ["python", "main.py"]
"""

from app.main import run

if __name__ == "__main__":
    run()
