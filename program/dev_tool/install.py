import subprocess
import shlex

from .install_venv import main as install_venv_main
from .install_deps import main as install_deps_main


def run(cmd):
    subprocess.run(shlex.split(cmd))


def main():
    install_venv_main()

    install_deps_main()


if __name__ == "__main__":
    main()
