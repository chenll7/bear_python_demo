from abc import ABC, abstractmethod
import json
from types import ModuleType
from typing import TypeVar, Generic
import importlib
import traceback

import colorama

from common_tool.check_update import main as check_update
from common_tool.log_mgr import logger, log_rule
from common_tool.abstract_config_mgr import AbstractConfigMgr, BaseConfig
from common_tool.abstract_controller import AbstractController, MyControllerError
from common_tool.abstract_arg_mgr import AbstractArgMgr, MyArgumentParserError
from common_tool.abstract_env_mgr import AbstractEnvMgr
from common_tool.util import run

T = TypeVar("T", bound=BaseConfig)


class AbstractEntry(ABC, Generic[T]):
    @property
    @abstractmethod
    def main_package(self) -> ModuleType:
        pass

    @property
    @abstractmethod
    def custom_config_mgr(self) -> AbstractConfigMgr[T]:
        pass

    @property
    @abstractmethod
    def custom_arg_mgr(self) -> AbstractArgMgr:
        pass

    @property
    @abstractmethod
    def custom_env_mgr(self) -> AbstractEnvMgr:
        pass

    def exit_callback(self, err=None):
        if err and type(err) not in [MyArgumentParserError, MyControllerError]:
            logger.error(traceback.format_exc())
        run("pause", shell=True)

    def _main(self):
        ####################################A
        # 初始化
        ####################################
        colorama.init()

        ####################################
        # 初始化配置，仅检查更新部分
        ####################################
        log_rule("Init Configuration For Check Update")
        self.custom_config_mgr.init_for_check_update()
        assert self.custom_config_mgr.check_update_config != None
        logger.info(
            f"\nConfiguration:\n{json.dumps(self.custom_config_mgr.check_update_config.to_json(),indent = 2)}\n"
        )

        ####################################
        # 检查更新
        ####################################
        log_rule("Check Update")
        if self.custom_config_mgr.check_update_config.check_update.enabled:
            check_update(
                main_package=self.main_package,
                target_dir_path=self.custom_config_mgr.check_update_config.check_update.target_dir_path,
            )

        ####################################
        # 初始化配置
        ####################################
        log_rule("Initializing Configuration")
        self.custom_config_mgr.init()
        assert self.custom_config_mgr.config != None
        logger.info(
            f"\nConfiguration:\n{json.dumps(self.custom_config_mgr.config.to_json(),indent = 2)}\n"
        )

        ####################################
        # 初始化环境信息
        ####################################
        log_rule("Initializing Environment Information")
        self.custom_env_mgr.init(main_package=self.main_package)

        ####################################
        # 执行Controller
        ####################################
        log_rule("Initializing Argument Parser")
        self.custom_arg_mgr.init()
        args = self.custom_arg_mgr.args

        ####################################
        # 执行Controller
        ####################################
        m = importlib.import_module(
            f"{self.main_package.__name__}.controller.{args.subparser_name}"
        )
        assert issubclass(m.Main, AbstractController)
        m.Main().main()

    def main(self):
        try:
            self._main()
        except Exception as err:
            self.exit_callback(err)
        else:
            self.exit_callback()
