import subprocess
import shlex
import shutil
import os
import tomllib
from pathlib import Path


PACKAGE_FOLDER_PATH = Path("package")
BUILD_FOLDER_PATH = Path("build")
RELEASE_FOLDER_PATH = Path("release")
INST_TMPL_FOLDER_PATH = Path("installer_template")


def run(cmd):
    subprocess.run(shlex.split(cmd))


print(f"Reading project name ...")
with open("pyproject.toml", "r") as pyproject_file:
    pyproject_content = pyproject_file.read()
    pyproject = tomllib.loads(pyproject_content)
project_name = pyproject["project"]["name"]
print(f"Reading project name is down. Project name is {project_name} .\n")

installer_dir_path = Path(RELEASE_FOLDER_PATH, project_name)
installer_path = Path(RELEASE_FOLDER_PATH, project_name)

run(rf'"tool\package.cmd"')

print(f"Recreating the folder {RELEASE_FOLDER_PATH} ...")
if RELEASE_FOLDER_PATH.exists():
    shutil.rmtree(RELEASE_FOLDER_PATH)
RELEASE_FOLDER_PATH.mkdir(parents=True, exist_ok=True)
print(f"Recreating the folder {RELEASE_FOLDER_PATH} is done.\n")

print("Creating the installer folder...")
shutil.copytree(INST_TMPL_FOLDER_PATH, installer_dir_path)
shutil.copytree(
    PACKAGE_FOLDER_PATH, Path(installer_dir_path, "package")
)
print("Creating the installer folder is done.\n")

print("Packaging the installer...")
print(installer_path)
shutil.make_archive(installer_path, 'zip', installer_dir_path)
print("Packaging the installer is done.\n")

print("Creating the updater...")
initial_cwd = os.getcwd()
os.chdir(installer_dir_path)
run('py "helper/script/create_updater.py" for-program')
os.chdir(initial_cwd)
print("Creating the updater is done.")