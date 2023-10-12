import os
from os import path
from typing import Optional
import tomllib
from typing import cast

from dotenv import load_dotenv

from .log_mgr import logger

REQUIRED_CONFIG_VERSION = '1'


class Config:

    class _CheckUpdate:
        def __init__(self, *, enabled, target_dir_path) -> None:
            self.enabled: bool = enabled
            self.target_dir_path: str = target_dir_path

        def to_json(self):
            return vars(self).copy()

    def init_for_check_update(self):
        # 读取配置
        with open('config.toml', 'rb') as f:
            config = tomllib.load(f)

        # 获取配置参数
        check_update = config.get('check_update', {})
        self.check_update: Config._CheckUpdate = Config._CheckUpdate(
            enabled=check_update.get('enabled', False),
            target_dir_path=check_update.get('target_dir_path', '.')
        )

    def init(
        self, *,
        main_package
    ):

        # 读取配置
        with open('config.toml', 'rb') as f:
            config = tomllib.load(f)

        # 读取环境变量注入配置
        load_dotenv()

        # 校验版本
        config_version = config['version']
        assert isinstance(config_version, str)
        if config_version != REQUIRED_CONFIG_VERSION:
            raise Exception(
                f'Configuration file version should be {REQUIRED_CONFIG_VERSION} instead of {config_version}'
            )
        logger.info(f'Configuration file version is {REQUIRED_CONFIG_VERSION}')
        self.config_version: str = config_version

        # 获取配置参数
        self.testing_env: str = os.environ.get('TESTING_ENV', 'production')
        self.app_name: str = (
            main_package.__name__+'-dev'
            if self.testing_env != 'production'
            else main_package.__name__
        )
        self.app_data_dir_path: str = path.join(
            cast(str, os.getenv('LOCALAPPDATA')),
            self.app_name
        )

    def to_json(self):
        json = vars(self).copy()
        if 'check_update' in json.keys():
            json['check_update'] = cast(
                Config._CheckUpdate,
                json['check_update']
            ).to_json()
        return json


def init_for_check_update():
    global _config
    if _config is None:
        _config = Config()
    _config.init_for_check_update()


def init(
    *,
    main_package
):
    global _config
    if _config is None:
        _config = Config()
    _config.init(main_package=main_package)


def get() -> Config:
    global _config
    if _config is None:
        raise Exception('Config is not initialized!')
    return _config


_config: Optional[Config] = None
