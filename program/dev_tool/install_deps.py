import subprocess
import shlex


def run(cmd):
    subprocess.run(shlex.split(cmd))


def main():
    print("Installing packages...")
    run(
        '"venv/Scripts/python" -m pip install --upgrade --no-index --find-links=./dependency -e .'
    )
    print("Installing packages is done.")


if __name__ == "__main__":
    main()
