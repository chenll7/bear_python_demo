import subprocess
import shlex
from os import path


def run(cmd):
    subprocess.run(shlex.split(cmd))


if not path.exists("venv"):
    print("Installing venv...")
    run("py -m venv venv")
    print("Installing venv is done.")

print("Installing packages...")
run('"venv/Scripts/python" -m pip install --upgrade --no-index --find-links=./package bear_python_demo')
print("Installing packages is done.")
