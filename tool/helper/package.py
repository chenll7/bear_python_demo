import subprocess
import shlex
import shutil
from os import path

PACKAGE_FOLDER_PATH = "package"
BUILD_FOLDER_PATH = "build"


def run(cmd):
    subprocess.run(shlex.split(cmd))


print(f"Deleting folder {PACKAGE_FOLDER_PATH} ...")
if path.exists(PACKAGE_FOLDER_PATH):
    shutil.rmtree(PACKAGE_FOLDER_PATH)
print(f"Deleting folder {PACKAGE_FOLDER_PATH} is done.\n")


print(f"Deleting folder {BUILD_FOLDER_PATH} ...")
if path.exists(BUILD_FOLDER_PATH):
    shutil.rmtree(BUILD_FOLDER_PATH)
print(f"Deleting folder {BUILD_FOLDER_PATH} is done.\n")

print("Packaging...")
run(
    rf"python -m pip wheel -w {PACKAGE_FOLDER_PATH} --no-index --find-links ./dependency --disable-pip-version-check ."
)
print("Packaging is done.\n")
