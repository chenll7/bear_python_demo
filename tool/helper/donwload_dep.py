import subprocess
import shlex
from os import path
import shutil


def run(cmd):
    subprocess.run(shlex.split(cmd))


folder_path = "dependency"
print(f"Deleting folder {folder_path} ...")
if path.exists(folder_path):
    shutil.rmtree(folder_path)
print(f"Deleting folder {folder_path} is done.\n")

run(
    rf'python -m pip download -d "{folder_path}" --disable-pip-version-check setuptools'
)
run(
    rf'python -m pip download -d "{folder_path}" --disable-pip-version-check setuptools-scm'
)
run(rf'python -m pip download -d "{folder_path}" --disable-pip-version-check wheel')
run(rf'python -m pip download -d "{folder_path}" --disable-pip-version-check .')
