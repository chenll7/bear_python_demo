import os
import zipfile
import tempfile
from os import path
import importlib.util
import sys

import bear_python_demo as main_package
from bear_python_demo import _version
from bear_python_demo.util.console_mgr import console
from bear_python_demo.util import config_mgr

PACKAGE_FOLDER_PATH = 'package'


def main():
    ####################################
    # 初始化
    ####################################
    current_version_str = _version.version
    console.log('Current version: {}'.format(current_version_str))
    console.log('Package name: {}'.format(main_package.__name__))

    ####################################
    # 读取配置
    ####################################
    config = config_mgr.get()
    target_dir_path = config.check_update.target_dir_path

    ####################################
    # 找包
    ####################################
    package_dir_path = path.join(
        target_dir_path,
        PACKAGE_FOLDER_PATH
    )
    for file_name in os.listdir(package_dir_path):
        if file_name.startswith(main_package.__name__):
            break
    else:
        raise Exception('Corresponding local wheel package not found!')
    file_path = path.join(PACKAGE_FOLDER_PATH, file_name)
    console.log('Local wheel package {} found.'.format(file_path), "")

    ####################################
    # 解压包
    ####################################
    console.log('Extract file from local wheel package...')
    with (
        tempfile.TemporaryDirectory() as tmp_dir_path,
        zipfile.ZipFile(file_path, 'r') as zip_file
    ):
        console.log('Temprary folder path: {}'.format(tmp_dir_path))
        zip_file.extract(main_package.__name__+'/_version.py', tmp_dir_path)
        tmp_file_path = path.join(
            tmp_dir_path, main_package.__name__+'/_version.py'
        )
        console.log('Extract file to {}'.format(tmp_file_path))

        spec = importlib.util.spec_from_file_location(
            "_version", tmp_file_path
        )
        if spec is None:
            raise Exception('Can not find _version file!')
        local_wheel_version = importlib.util.module_from_spec(spec)
        spec_loader = spec.loader
        if spec_loader is None:
            raise Exception('Can not get spec loader!')
        spec_loader.exec_module(local_wheel_version)
        local_wheel_version_str = local_wheel_version.version
        console.log('Local wheel version: {}'.format(local_wheel_version_str))

    if local_wheel_version_str == current_version_str:
        console.log('[green]No update![/]', "")
    else:
        console.log('[bold red]Update found![/]\nLocal wheel version is [blue]{}[/] ,\nbut current version is [red]{}[/] .\nPlease run install.cmd to reinstall the application.\n'.format(
            local_wheel_version_str,
            current_version_str
        ))
        sys.exit()


if __name__ == '__main__':
    main()
