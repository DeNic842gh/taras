"""
Application entry point.

Run with Poetry (dependencies are in the project venv, not system Python):
    poetry install
    poetry run python main.py

Or:
    poetry run serve
"""

try:
    from app.main import run
except ModuleNotFoundError:
    print(
        "Missing dependencies. Use Poetry:\n"
        "  poetry install\n"
        "  poetry run python main.py\n"
        "\n"
        "Or activate the venv:\n"
        "  poetry shell\n"
        "  python main.py"
    )
    raise

if __name__ == "__main__":
    run()
