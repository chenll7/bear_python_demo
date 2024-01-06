from zipfile import ZipFile
import os
import re
from tempfile import NamedTemporaryFile
from collections import deque
import sys
from enum import Enum
from pathlib import Path


class Mode(Enum):
    FOR_PROGRAM = 1
    FOR_DATA = 2

SUFFIX = {
    Mode.FOR_PROGRAM: "for_program",
    Mode.FOR_DATA: "for_data"
}

PATH_SEP = re.escape(os.sep)

UPDATING_SCOPE = {
    Mode.FOR_PROGRAM: [
        rf"helper{PATH_SEP}.+",
        rf"package{PATH_SEP}.+",
        rf"[^\\/]+\.cmd",
    ],
    Mode.FOR_DATA: [rf"config.toml"],
}

APP_NAME = 'bear_python_demo'

SRC_ROOT_DIR_PATH = Path(".")

TGT_ROOT_DIR_NAME = "bear_python_demo_updater"
CONTENT_DIR_REL_PATH = Path("content")

UPDATE_CMD_FILE_CONTENT = """\
@echo off

call py ./helper/script/update.py

pause
"""


UPDATE_PY_FILE_CONTENT= '''\
import os
import shutil
from collections import deque
from pathlib import Path

SRC_ROOT_DIR_PATH = Path('content')
TGT_ROOT_DIR_PATH = Path('..')

def main():
    # 将content目录下的文件复制到目标目录
    print('Start to copy files...')
    to_check_stack = [Path('.')]
    to_add_queue = deque([])
    while len(to_check_stack) > 0:
        dir_rel_path = to_check_stack.pop()
        to_add_queue.append(dir_rel_path)
        dir_path = Path(SRC_ROOT_DIR_PATH, dir_rel_path)
        for item_path in dir_path.iterdir():
            item_rel_path = Path(dir_rel_path, item_path.name)
            if item_path.is_file():
                to_add_queue.append(item_rel_path)
            elif item_path.is_dir():
                to_check_stack.append(item_rel_path)
    while len(to_add_queue) > 0:
        item_rel_path = to_add_queue.popleft()
        src_item_path = Path(SRC_ROOT_DIR_PATH, item_rel_path)
        tgt_item_path = Path(TGT_ROOT_DIR_PATH, item_rel_path)
        print(f'Copying {src_item_path} to {tgt_item_path}...')
        if src_item_path.is_dir():
            tgt_item_path.mkdir(parents=True, exist_ok=True)
        elif src_item_path.is_file():
            shutil.copy2(src_item_path, tgt_item_path)


if __name__ == '__main__':
    main()

'''


def main(mode):
    suffix = SUFFIX[mode]
    tgt_root_dir_name = f"{TGT_ROOT_DIR_NAME}_{suffix}"
    updating_scope_pattern_str_list = UPDATING_SCOPE[mode]
    updating_scope_pattern_list = list(map(re.compile, updating_scope_pattern_str_list))

    print("Creating archive file...")
    with NamedTemporaryFile(delete=False) as update_cmd_file:
        update_cmd_file.write(UPDATE_CMD_FILE_CONTENT.encode())
        update_cmd_file_path = update_cmd_file.name

    with NamedTemporaryFile(delete=False) as update_py_file:
        update_py_file.write(UPDATE_PY_FILE_CONTENT.encode())
        update_py_file_path = update_py_file.name

    with ZipFile(Path("..",f"{tgt_root_dir_name}.zip"), "w") as z:
        written_item_path_list:list[Path]= []

        print(update_cmd_file_path)
        tgt_update_cmd_file_path = Path(tgt_root_dir_name, "update.cmd")
        z.write(update_cmd_file_path, tgt_update_cmd_file_path)
        written_item_path_list.append(tgt_update_cmd_file_path)

        print(update_py_file_path)
        tgt_update_py_file_path = Path(tgt_root_dir_name, "helper/script/update.py")
        z.write(update_py_file_path, tgt_update_py_file_path)
        written_item_path_list.append(tgt_update_py_file_path)

        to_check_stack = [Path(".")]
        to_add_stack = deque([])
        while len(to_check_stack) > 0:
            dir_rel_path = to_check_stack.pop()
            # to_add_stack.append(dir_rel_path)
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
            tgt_item_path = Path(tgt_root_dir_name, CONTENT_DIR_REL_PATH, APP_NAME, item_rel_path)
            if not any(
                UPDATING_SCOPE_PATTERN.match(str(item_rel_path))
                for UPDATING_SCOPE_PATTERN in updating_scope_pattern_list
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
    match sys.argv[1] if len(sys.argv) > 1 else None:
        case "for-program":
            mode = Mode.FOR_PROGRAM
        case "for-data":
            mode = Mode.FOR_DATA
        case _:
            raise Exception("An invalid option!")
    main(mode)
