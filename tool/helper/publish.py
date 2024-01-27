import subprocess
import shlex
import shutil
import os
from os import path
from zipfile import ZipFile


RELEASE_FOLDER_PATH = "release"
APP_NAME = 'bear_python_demo'
UPDATER_NAME = 'bear_python_demo_updater_for_program'
PUBLISH_PATH = path.expanduser("~/bear_base/active/tool-homemade/")


def run(cmd):
    subprocess.run(shlex.split(cmd))

installer_path = path.join(PUBLISH_PATH, APP_NAME)
if not path.exists(installer_path):
    raise Exception(f'No installer found in path {installer_path}')

run(rf'"tool\release.cmd"')

updater_file_path = path.join(RELEASE_FOLDER_PATH, f"{UPDATER_NAME}.zip")
print(f"Copying file {updater_file_path} to publish folder {PUBLISH_PATH}...")
shutil.copy2(updater_file_path, PUBLISH_PATH)
print(f"Copying file {updater_file_path} to publish folder {PUBLISH_PATH} is done.")

updater_file_in_publish_path = path.join(PUBLISH_PATH, f"{UPDATER_NAME}.zip")
print(f"Extracting updater file {updater_file_in_publish_path} ...")
with ZipFile(updater_file_in_publish_path, "r") as z:
    z.extractall(PUBLISH_PATH)
os.unlink(updater_file_in_publish_path)
print(f"Extracting updater file {updater_file_in_publish_path} is done.")

updater_dir_in_publish_path = path.join(PUBLISH_PATH, UPDATER_NAME)
print(f"Running updater folder {updater_dir_in_publish_path} ...")
initial_cwd = os.getcwd()
os.chdir(updater_dir_in_publish_path)
run('py "helper/script/update.py"')
os.chdir(initial_cwd)
shutil.rmtree(updater_dir_in_publish_path)
print(f"Running updater folder {updater_dir_in_publish_path} is done.")