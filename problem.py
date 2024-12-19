import os
import shutil
import subprocess
import time
from pathlib import Path

UV_EXE = Path(shutil.which("uv"))
TEMP_PATH = Path(os.environ["TEMP"])
TARGET_PATH = TEMP_PATH / f"uv-pip-install-{time.time_ns()}"
REQUIREMENTS_PATH = TARGET_PATH / "requirements.txt"
TARGET_VENV_PATH = TARGET_PATH / ".venv"


# simulate cloning of some Git repo containing a requirements.txt file
print("----- simulate clone of git repo -----")
print(TARGET_PATH)
TARGET_PATH.mkdir()
with open(REQUIREMENTS_PATH, 'w') as file:
    file.writelines(["pyyaml==6.0.1\n", "xmltodict==0.13.0"])


print("----- Create venv with 'uv' -----")
with subprocess.Popen(
    [
        UV_EXE,
        "venv",
        "--no-progress",
        "--color",
        "never",
        TARGET_VENV_PATH,
    ],
    stdout=subprocess.PIPE,
    bufsize=1,
    universal_newlines=True,
) as proc:
    for line in proc.stdout:
        print(line, end="")


print("----- Install dependencies with 'uv' -----")
with subprocess.Popen(
    [
        UV_EXE,
        "pip",
        "install",
        "--directory",
        TARGET_PATH,
        "--no-progress",
        "--color",
        "never",
        "-r",
        REQUIREMENTS_PATH,
    ],
    stdout=subprocess.PIPE,
    bufsize=1,
    universal_newlines=True,
    cwd=TARGET_PATH,
) as proc:
    for line in proc.stdout:
        print(line, end="")

