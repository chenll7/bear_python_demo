from zipfile import ZipFile
import os
import re
from tempfile import NamedTemporaryFile
from collections import deque
from pathlib import Path
import tomllib
import shutil

SEP = re.escape(os.sep)

IGNORE_PATH_PATTERN_STR_LIST = [
    rf"archive{SEP}.+",
    rf"\.git{SEP}.+",
    rf"venv{SEP}.+",
    rf"log{SEP}.+",
    rf".*\.egg-info{SEP}.+",
    rf"config.toml",
    rf"(?:[^{SEP}]+{SEP})*__pycache__{SEP}.+",
]

SRC_ROOT_DIR_PATH = Path(".")

TGT_ROOT_DIR_PATH = Path("archive/")

def main():
    if TGT_ROOT_DIR_PATH.exists():
        shutil.rmtree(TGT_ROOT_DIR_PATH)
    TGT_ROOT_DIR_PATH.mkdir(parents=True)

    IGNORE_PATH_PATTERN_LIST = list(map(re.compile, IGNORE_PATH_PATTERN_STR_LIST))

    with open("pyproject.toml", "rb") as f:
        pyproject_conifg = tomllib.load(f)
    app_name = pyproject_conifg["project"]["name"]

    print("Creating archive file...")
    with ZipFile(Path(TGT_ROOT_DIR_PATH, f'{app_name}.zip'), "w") as z:
        written_item_path_list:list[Path] = []

        to_check_stack = [Path(".")]
        to_add_stack = deque([])
        while len(to_check_stack) > 0:
            dir_rel_path = to_check_stack.pop()
            dir_path = Path(SRC_ROOT_DIR_PATH, dir_rel_path)
            for item_path in dir_path.iterdir():
                item_rel_path = Path(dir_rel_path, item_path.name)
                if item_path.is_file():
                    to_add_stack.append(item_rel_path)
                elif item_path.is_dir():
                    to_check_stack.append(item_rel_path)
        while len(to_add_stack) > 0:
            item_rel_path = to_add_stack.popleft()
            src_item_path = Path(SRC_ROOT_DIR_PATH, item_rel_path)
            tgt_item_path = Path(item_rel_path)
            if any(
                IGNORE_PATH_PATTERN.match(str(item_rel_path))
                for IGNORE_PATH_PATTERN in IGNORE_PATH_PATTERN_LIST
            ):
                print(f'Not pick: {src_item_path}')
                continue
            else:
                print(f'Pick: {src_item_path}')
                z.write(
                    src_item_path,
                    tgt_item_path
                )
                written_item_path_list.append(tgt_item_path)

        written_item_path_list_str = '\n'.join(map(str, written_item_path_list))
        print(f'Following file has written to the zip file:\n{written_item_path_list_str}\n')


if __name__ == "__main__":
    main()
