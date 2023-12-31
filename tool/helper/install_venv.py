import subprocess
import shlex
import shutil
from pathlib import Path


def run(cmd):
    subprocess.run(shlex.split(cmd))


run('py "-3.11" -m venv venv')

print("Copying pip.ini ...")
shutil.copy2(Path.home() / "pip/pip.ini", "venv/pip.ini")
print("Copying pip.ini is done.")
