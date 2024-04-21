import os
import shutil
from collections import deque
from pathlib import Path
import tomllib
import zipfile

TGT_ROOT_DIR_PATH = Path('.')

def main():

    with open("pyproject.toml", "rb") as f:
        pyproject_conifg = tomllib.load(f)
    app_name = pyproject_conifg["project"]["name"]

    zip_file_path = Path('..', f'{app_name}.zip')

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for item_path in zip_ref.namelist():
            print (item_path)
        zip_ref.extractall(TGT_ROOT_DIR_PATH)

if __name__ == '__main__':
    main()