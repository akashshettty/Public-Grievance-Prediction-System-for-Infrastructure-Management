from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_PATH = PROJECT_ROOT / "src" / "dashboard" / "app.py"


def main() -> None:
    command = [sys.executable, "-m", "streamlit", "run", str(APP_PATH)]
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
