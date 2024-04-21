from abc import ABC, abstractmethod
import tomllib
from pathlib import Path
from typing import cast
import os
from argparse import ArgumentParser

from program.common_tool.log_mgr import logger


class MyConfigParserError(Exception):
    pass


class MyArgumentParserError(Exception):
    pass


class MyArgumentParser(ArgumentParser):
    def error(self, message):
        logger.info(f"\n{self.format_help()}\n{message}")
        raise MyArgumentParserError(message)


class AbstractOptionMgr(ABC):
    def __init__(self):
        self.config = None
        self.env = None
        self.args = None

    @property
    @abstractmethod
    def required_config_version(self) -> str:
        pass

    def add_env(self) -> None:
        pass

    @abstractmethod
    def add_parses(self, root_parser: MyArgumentParser) -> None:
        pass

    def init(self):
        ########################################
        # 加载配置
        ########################################
        # 读取配置
        with open("config.toml", "rb") as f:
            self.config = tomllib.load(f)
        logger.info(f"\nConfig:\n{self.config}")

        # 校验版本
        config_version = self.config["version"]["version"]
        if config_version != self.required_config_version:
            raise MyConfigParserError(
                f"Configuration file version should be {self.required_config_version} instead of {config_version}"
            )
        logger.info(f"Configuration file version is {self.required_config_version}")

        ########################################
        # 加载环境信息
        ########################################
        testing_env = self.config["testing_env"]["testing_env"]
        with open("pyproject.toml", "rb") as f:
            pyproject_conifg = tomllib.load(f)
        original_app_name = pyproject_conifg["project"]["name"]
        app_name = (
            original_app_name + "-dev"
            if testing_env != "production"
            else original_app_name
        )
        app_data_dir_path = Path(cast(str, os.getenv("LOCALAPPDATA")), app_name)
        self.env = {
            "original_app_name": original_app_name,
            "app_name": app_name,
            "app_data_dir_path": app_data_dir_path,
        }
        self.add_env()

        ########################################
        # 加载命令行
        ########################################
        root_parser = MyArgumentParser(prog="PROGRAM")
        self.add_parses(root_parser)
        self.args = root_parser.parse_args()
        if self.args.subparser_name == None:
            root_parser.print_help()
            raise MyArgumentParserError("Sub-command needed!")
