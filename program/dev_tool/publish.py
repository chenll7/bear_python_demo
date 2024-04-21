import subprocess
import shlex
import shutil
import os
from pathlib import Path
import tomllib

from .create_archive import main as create_archive_main

PUBLISH_PARENT_PATH = Path("~/bear_base/active/app/").expanduser()


def run(cmd):
    subprocess.run(shlex.split(cmd))


def main():
    # 创建归档文件路径
    create_archive_main()

    # 获得归档文件路径和发布路径
    with open("pyproject.toml", "rb") as f:
        pyproject_conifg = tomllib.load(f)
    app_name = pyproject_conifg["project"]["name"]
    archive_path = Path("archive", f"{app_name}.zip")
    publish_path = Path(PUBLISH_PARENT_PATH, app_name)

    # 归档文件拷贝到发布目录父目录
    print(
        f"Copying file {archive_path} to the parent folder of the publish folder {PUBLISH_PARENT_PATH}..."
    )
    archive_in_publish_parent_path = Path(PUBLISH_PARENT_PATH, f"{app_name}.zip")
    shutil.copy2(archive_path, archive_in_publish_parent_path)
    print(
        f"Copying file {archive_path} to the parent folder of the publish folder {PUBLISH_PARENT_PATH} is done.\n"
    )

    # 从归档文件更新发布目录
    print(f"Updating from the archive...")
    initial_cwd = os.getcwd()
    os.chdir(publish_path)
    run("py -m program.dev_tool.update_from_archive")
    os.chdir(initial_cwd)
    print(f"Updating from the archive is done.\n")

    # 删除拷贝到发布目录父目录的归档文件
    print(f"Deleting the archive in the parent folder of the publish folder...")
    archive_in_publish_parent_path.unlink()
    print(f"Deleting the archive in the parent folder of the publish folder is done.\n")


if __name__ == "__main__":
    main()
