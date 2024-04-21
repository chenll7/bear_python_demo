import subprocess
import shlex
from os import path
import shutil
from pathlib import Path

FOLDER_PATH = Path("dependency")

def run(cmd):
    subprocess.run(shlex.split(cmd))

def main():
    #####################
    # Deleting the Folder
    #####################
    print(f"Deleting folder {FOLDER_PATH} ...")
    if path.exists(FOLDER_PATH):
        shutil.rmtree(FOLDER_PATH)
    print(f"Deleting folder {FOLDER_PATH} is done.\n")

    #####################
    # Downloading Deps
    #####################
    run(
        rf'python -m pip download -d "{FOLDER_PATH}" --disable-pip-version-check setuptools'
    )
    # run(rf'python -m pip download -d "{FOLDER_PATH}" --disable-pip-version-check setuptools-scm')
    run(rf'python -m pip download -d "{FOLDER_PATH}" --disable-pip-version-check wheel')
    run(rf'python -m pip download -d "{FOLDER_PATH}" --disable-pip-version-check .')

if __name__ == '__main__':
    main()


