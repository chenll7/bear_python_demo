import subprocess
import shlex
import shutil
import os
from os import path
import tomllib


PACKAGE_FOLDER_PATH = "package"
BUILD_FOLDER_PATH = "build"
RELEASE_FOLDER_PATH = "release"
INST_TMPL_FOLDER_PATH = "installer_template"


def run(cmd):
    subprocess.run(shlex.split(cmd))


print(f"Reading project name ...")
with open("pyproject.toml", "r") as pyproject_file:
    pyproject_content = pyproject_file.read()
    pyproject = tomllib.loads(pyproject_content)
project_name = pyproject["project"]["name"]
print(f"Reading project name is down. Project name is {project_name} .\n")

installer_path = path.join(RELEASE_FOLDER_PATH, project_name)

run(rf'"tool\package.cmd"')

print(f"Recreating the folder {RELEASE_FOLDER_PATH} ...")
if path.exists(RELEASE_FOLDER_PATH):
    shutil.rmtree(RELEASE_FOLDER_PATH)
os.mkdir(RELEASE_FOLDER_PATH)
print(f"Recreating the folder {RELEASE_FOLDER_PATH} is done.\n")

print("Creating the installer...")
shutil.copytree(INST_TMPL_FOLDER_PATH, installer_path)
shutil.copytree(
    PACKAGE_FOLDER_PATH, path.join(installer_path, "package")
)
print("Creating the installer is done.\n")

print("Creating the updater...")
initial_cwd = os.getcwd()
os.chdir(installer_path)
run('py "helper/script/create_updater.py" for-program')
os.chdir(initial_cwd)
print("Creating the updater is done.")