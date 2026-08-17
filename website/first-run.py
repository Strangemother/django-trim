#!/usr/bin/env python3
"""Create the website environment, migrate the database, and run Django."""

from pathlib import Path
import os
import subprocess
import sys
import venv


WEBSITE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = WEBSITE_DIR / "primary"
ENV_DIR = WEBSITE_DIR / "env"


def run(*command):
    """Run a command from the website project directory."""
    subprocess.run(command, cwd=PROJECT_DIR, check=True)


def main():
    """Set up the local environment and start the development server."""
    if not (ENV_DIR / "pyvenv.cfg").exists():
        print(f"Creating virtual environment: {ENV_DIR}")
        venv.EnvBuilder(with_pip=True).create(ENV_DIR)

    python = ENV_DIR / "Scripts" / "python.exe"
    if not python.exists():
        python = ENV_DIR / "bin" / "python"

    run(python, "-m", "pip", "install", "-r", str(WEBSITE_DIR / "requirements.txt"))
    run(python, "manage.py", "migrate")
    os.chdir(PROJECT_DIR)
    os.execv(str(python), [str(python), "manage.py", "runserver"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nDevelopment server stopped.")
