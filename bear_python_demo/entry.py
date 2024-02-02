from argparse import ArgumentParser

import bear_python_demo as main_package
from bear_python_demo.helper.config_mgr import config_mgr, Config
from bear_python_demo.helper.arg_mgr import arg_mgr
from bear_python_demo.helper.env_mgr import env_mgr
from common_tool.log_mgr import logger, log_rule, C, Color
from common_tool.abstract_entry import AbstractEntry
from common_tool.abstract_config_mgr import AbstractConfigMgr
from common_tool.abstract_arg_mgr import AbstractArgMgr
from common_tool.abstract_env_mgr import AbstractEnvMgr


class Entry(AbstractEntry[Config]):
    @property
    def main_package(self):
        return main_package

    @property
    def custom_config_mgr(self) -> AbstractConfigMgr[Config]:
        return config_mgr

    @property
    def custom_arg_mgr(self) -> AbstractArgMgr:
        return arg_mgr

    @property
    def custom_env_mgr(self) -> AbstractEnvMgr:
        return env_mgr


def main():
    Entry().main()


if __name__ == "__main__":
    main()
