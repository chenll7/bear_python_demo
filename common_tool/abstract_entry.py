from abc import ABC, abstractmethod
import json
from types import ModuleType
from argparse import ArgumentParser
import importlib
import subprocess
import shlex

import colorama

from common_tool.check_update import main as check_update
from common_tool.log_mgr import logger, log_rule
from common_tool.abstract_config import AbstractConfig
from common_tool.abstract_controller import AbstractController

def run(cmd, *args, **kwargs):
    subprocess.run(shlex.split(cmd), *args, **kwargs)

class AbstractEntry(ABC):
    @property
    @abstractmethod
    def main_package(self) -> ModuleType:
        pass

    @property
    @abstractmethod
    def custom_config(self) -> AbstractConfig:
        pass

    @abstractmethod
    def add_parses(self, subparsers: ArgumentParser) -> None:
        pass

    def exit_callback(self, err=None):
        run('pause', shell = True)

    def _main(self):
        ####################################A
        # 初始化
        ####################################
        colorama.init()

        ####################################
        # 初始化配置，仅检查更新部分
        ####################################
        log_rule("Init Configuration For Check Update")
        self.custom_config.init_for_check_update()
        logger.info(
            f"\nConfiguration:\n{json.dumps(self.custom_config.to_json(),indent = 2)}\n"
        )

        ####################################
        # 检查更新
        ####################################
        log_rule("Check Update")
        if self.custom_config.check_update.enabled:
            need_to_update = check_update(
                main_package=self.main_package, custom_config=self.custom_config
            )
            if need_to_update:
                return

        ####################################
        # 初始化配置
        ####################################
        log_rule("Init Configuration")
        self.custom_config.init(main_package=self.main_package)
        logger.info(
            f"\nConfiguration:\n{json.dumps(self.custom_config.to_json(), indent = 2)}\n"
        )

        ####################################
        # 执行Controller
        ####################################
        root_parser = ArgumentParser(prog='PROGRAM')
        self.add_parses(root_parser)
        args = root_parser.parse_args()
        if args.subparser_name == None:
            logger.info('Sub-command needed!')
            root_parser.print_help()
            return
        m = importlib.import_module(f'{self.main_package.__name__}.controller.{args.subparser_name}')
        assert issubclass(m.Main, AbstractController)
        m.Main().main()

    def main(self):
        try:
            self._main()
        except Exception as err:
            self.exit_callback(err)
        else:
            self.exit_callback()
