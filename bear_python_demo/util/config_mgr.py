import os
from os import path
from typing import Optional
import tomllib
from typing import cast

from dotenv import load_dotenv

import bear_python_demo
from bear_python_demo.util.console_mgr import console

REQUIRED_CONFIG_VERSION = '1'


class Config:

    class _CheckUpdate:
        def __init__(self, *, enabled, target_dir_path) -> None:
            self.enabled: bool = enabled
            self.target_dir_path: str = target_dir_path

        def to_json(self):
            return vars(self).copy()

    def __init__(self):

        # 读取配置
        with open('config.toml', 'rb') as f:
            config = tomllib.load(f)

        # 读取环境变量注入配置
        load_dotenv()

        # 校验版本
        config_version = config['version']
        assert isinstance(config_version, str)
        if config_version != REQUIRED_CONFIG_VERSION:
            raise Exception('Configuration file version should be {} instead of {}'.format(
                REQUIRED_CONFIG_VERSION, config_version
            ))
        console.log('Configuration file version is {}'.format(
            REQUIRED_CONFIG_VERSION
        ))
        self.config_version: str = config_version

        # 获取配置参数
        self.app_name: str = (
            bear_python_demo.__name__+'-dev'
            if config.get('debug_mode', False)
            else bear_python_demo.__name__
        )
        self.app_data_dir_path: str = path.join(
            cast(str, os.getenv('LOCALAPPDATA')),
            self.app_name
        )
        check_update = config.get('check_update', {})
        self.check_update: Config._CheckUpdate = Config._CheckUpdate(
            enabled=check_update.get('enabled', False),
            target_dir_path=check_update.get('target_dir_path', '.')
        )
        self.testing_env: str = os.environ.get('TESTING_ENV', 'production')

    def to_json(self):
        json = vars(self).copy()
        json['check_update'] = cast(
            Config._CheckUpdate,
            json['check_update']
        ).to_json()
        return json


def init():
    global _config
    _config = Config()


def get() -> Config:
    if _config is None:
        raise Exception('Config is not initialized!')
    return _config


_config: Optional[Config] = None
