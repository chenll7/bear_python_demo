from zipfile import ZipFile
import os
from os import path
import re
from tempfile import NamedTemporaryFile
from collections import deque
import sys
from enum import Enum


class Mode(Enum):
    FOR_PROGRAM = 1
    FOR_DATA = 2

SUFFIX = {
    Mode.FOR_PROGRAM: "for_program",
    Mode.FOR_DATA: "for_data"
}

UPDATING_SCOPE = {
    Mode.FOR_PROGRAM: [
        r"\.[\\/]helper(?:[\\/].+)?",
        r"\.[\\/]package(?:[\\/].+)?",
        r"\.[\\/][^\\/]+\.cmd(?:[\\/].+)?",
    ],
    Mode.FOR_DATA: [r"\.[\\/]config.toml"],
}

APP_NAME = 'bear_python_demo'

SRC_ROOT_DIR_PATH = "."

TGT_ROOT_DIR_NAME = "bear_python_demo_updater"
CONTENT_DIR_REL_PATH = "content"

UPDATE_CMD_FILE_CONTENT = """\
@echo off

call py ./helper/script/update.py

pause
"""


UPDATE_PY_FILE_CONTENT= '''\
import os
from os import path
import shutil
from collections import deque

SRC_ROOT_DIR_PATH = 'content'
TGT_ROOT_DIR_PATH = '..'

def main():
    # 将content目录下的文件复制到目标目录
    print('Start to copy files...')
    to_check_stack = ['.']
    to_add_queue = deque([])
    while len(to_check_stack) > 0:
        dir_rel_path = to_check_stack.pop()
        to_add_queue.append(dir_rel_path)
        dir_path = path.join(SRC_ROOT_DIR_PATH, dir_rel_path)
        for item_name in os.listdir(dir_path):
            item_path = path.join(dir_path, item_name)
            item_rel_path = path.join(dir_rel_path, item_name)
            if path.isfile(item_path):
                to_add_queue.append(item_rel_path)
            elif path.isdir(item_path):
                to_check_stack.append(item_rel_path)
    while len(to_add_queue) > 0:
        item_rel_path = to_add_queue.popleft()
        src_item_path = path.join(SRC_ROOT_DIR_PATH, item_rel_path)
        tgt_item_path = path.join(TGT_ROOT_DIR_PATH, item_rel_path)
        print(f'Copying {src_item_path} ...')
        if path.isdir(src_item_path):
            if not path.exists(tgt_item_path):
                os.makedirs(tgt_item_path)
        elif path.isfile(src_item_path):
            shutil.copy2(src_item_path, tgt_item_path)


if __name__ == '__main__':
    main()
'''


def main(mode):
    suffix = SUFFIX[mode]
    tgt_root_dir_name = f"{TGT_ROOT_DIR_NAME}_{suffix}"
    updating_scope_pattern_str_list = UPDATING_SCOPE[mode]
    updating_scope_pattern_list = list(map(re.compile, updating_scope_pattern_str_list))

    # # 避免在installer里头执行
    # working_dir_name = path.basename(os.getcwd())
    # if working_dir_name == 'ssh_mgr_installer':
    #     print('Can not execute archiving for update in a installer!')
    #     return

    print("Creating archive file...")
    with NamedTemporaryFile(delete=False) as update_cmd_file:
        update_cmd_file.write(UPDATE_CMD_FILE_CONTENT.encode())
        update_cmd_file_path = update_cmd_file.name

    with NamedTemporaryFile(delete=False) as update_py_file:
        update_py_file.write(UPDATE_PY_FILE_CONTENT.encode())
        update_py_file_path = update_py_file.name

    with ZipFile(path.join("..",f"{tgt_root_dir_name}.zip"), "w") as z:
        print(update_cmd_file_path)
        z.write(update_cmd_file_path, path.join(tgt_root_dir_name, "update.cmd"))

        print(update_py_file_path)
        z.write(
            update_py_file_path, path.join(tgt_root_dir_name, "helper/script/update.py")
        )


        to_check_stack = ["."]
        to_add_stack = deque([])
        while len(to_check_stack) > 0:
            dir_rel_path = to_check_stack.pop()
            to_add_stack.append(dir_rel_path)
            dir_path = path.join(SRC_ROOT_DIR_PATH, dir_rel_path)
            for item_name in os.listdir(dir_path):
                item_path = path.join(dir_path, item_name)
                item_rel_path = path.join(dir_rel_path, item_name)
                if path.isfile(item_path):
                    to_add_stack.append(item_rel_path)
                elif path.isdir(item_path):
                    to_check_stack.append(item_rel_path)
        while len(to_add_stack) > 0:
            item_rel_path = to_add_stack.popleft()
            src_item_path = path.join(SRC_ROOT_DIR_PATH, item_rel_path)
            tgt_item_path = path.join(tgt_root_dir_name, CONTENT_DIR_REL_PATH, APP_NAME, item_rel_path)
            if not any(
                UPDATING_SCOPE_PATTERN.match(item_rel_path)
                for UPDATING_SCOPE_PATTERN in updating_scope_pattern_list
            ):
                print(f'Not pick: {item_rel_path}')
                continue
            else:
                print(f'Pick: {item_rel_path}')
                z.write(
                    src_item_path,
                    tgt_item_path
                )


if __name__ == "__main__":
    match sys.argv[1] if len(sys.argv) > 1 else None:
        case "for-program":
            mode = Mode.FOR_PROGRAM
        case "for-data":
            mode = Mode.FOR_DATA
        case _:
            raise Exception("An invalid option!")
    main(mode)
