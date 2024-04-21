import subprocess
import shlex
import shutil
from pathlib import Path


VENV_PATH = Path("venv")


def run(cmd):
    subprocess.run(shlex.split(cmd))


def main():
    #####################
    # Install Venv
    #####################
    if VENV_PATH.exists():
        print(f"The venv folder path {VENV_PATH} exists!")
        return
    run(f'py "-3.11" -m venv "{VENV_PATH}"')

    #####################
    # Copy pip.ini
    #####################
    print("Copying pip.ini ...")
    pip_ini_path = Path.home() / "pip/pip.ini"
    if pip_ini_path.exists():
        shutil.copy2(Path.home() / "pip/pip.ini", "venv/pip.ini")
    else:
        print("The pip.ini does not exist.")
    print("Copying pip.ini is done.")


if __name__ == "__main__":
    main()
