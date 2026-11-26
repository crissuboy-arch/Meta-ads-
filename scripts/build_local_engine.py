"""Bundle Python and agent configs for Tauri, using the CI runner's platform."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
subprocess.run([
    sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onedir",
    "--name", "local-engine", "--distpath", str(ROOT / "src-tauri/runtime"),
    "--workpath", str(ROOT / "build/local-engine"), "--paths", str(ROOT),
    "--collect-submodules", "local_engine", "--add-data", str(ROOT / "configs") + ":configs",
    str(ROOT / "local_engine/server.py"),
], cwd=ROOT, check=True)
