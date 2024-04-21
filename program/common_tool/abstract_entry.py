from abc import ABC, abstractmethod
import json
from types import ModuleType
from typing import TypeVar, Generic
import importlib
import traceback

import colorama

from program.common_tool.log_mgr import logger, log_rule, C
from program.common_tool.abstract_controller import (
    AbstractController,
    MyControllerError,
)
from program.common_tool.abstract_option_mgr import (
    AbstractOptionMgr,
    MyConfigParserError,
    MyArgumentParserError,
)
from program.common_tool.util import run


class AbstractEntry(ABC):
    def __init__(self):
        self.controller_name = None

    @property
    @abstractmethod
    def option_mgr(self) -> AbstractOptionMgr:
        pass

    def exit_callback(self, controller_name, err=None):
        if err and type(err) not in [MyArgumentParserError, MyControllerError]:
            logger.error(traceback.format_exc())
        run("pause", shell=True)

    def _main(self):
        ####################################As
        # 初始化colorama
        ####################################
        colorama.init()

        ####################################
        # 初始化配置信息
        ####################################
        log_rule("Initializing Option Info")
        self.option_mgr.init()
        args = self.option_mgr.args
        logger.info(args)
        assert isinstance(args, object)

        ####################################
        # 执行Controller
        ####################################
        m = importlib.import_module(f"program.main.controller.{args.subparser_name}")
        assert issubclass(m.Main, AbstractController)
        m.Main().main()

    def main(self):
        try:
            self._main()
        except Exception as err:
            self.exit_callback(self.controller_name, err)
        else:
            self.exit_callback(self.controller_name)
