import os
import zipfile
import tempfile
from os import path
import importlib.util
import sys

from colorama import Fore

import bear_python_demo as main_package
from bear_python_demo import _version
from bear_python_demo.util.log_mgr import logger, C, Color
from bear_python_demo.util import config_mgr

PACKAGE_FOLDER_PATH = 'package'


def main():
    ####################################
    # 初始化
    ####################################
    current_version_str = _version.version
    logger.info(f'Current version: {current_version_str}')
    logger.info(f'Package name: {main_package.__name__}')

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
    logger.info(f'Local wheel package {file_path} found.\n')

    ####################################
    # 解压包
    ####################################
    logger.info('Extract file from local wheel package...')
    with (
        tempfile.TemporaryDirectory() as tmp_dir_path,
        zipfile.ZipFile(file_path, 'r') as zip_file
    ):
        logger.info(f'Temprary folder path: {tmp_dir_path}')
        zip_file.extract(main_package.__name__+'/_version.py', tmp_dir_path)
        tmp_file_path = path.join(
            tmp_dir_path, main_package.__name__+'/_version.py'
        )
        logger.info(f'Extract file to {tmp_file_path}')

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
        logger.info(f'Local wheel version: {local_wheel_version_str}')

    if local_wheel_version_str == current_version_str:
        logger.info(C((Color(Fore.GREEN), 'No update!', Color(Fore.RESET))))
    else:
        logger.info(C((
            Color(Fore.RED), f'Update found!', Color(Fore.RESET),
            f'\nLocal wheel version is ',
            Color(Fore.BLUE), local_wheel_version_str, Color(Fore.RESET),
            f' ,\nbut current version is ',
            Color(Fore.RED), current_version_str, Color(Fore.RESET),
            f' .\nPlease run install.cmd to reinstall the application.\n'
        )))
        sys.exit()


if __name__ == '__main__':
    main()
