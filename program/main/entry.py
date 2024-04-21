from argparse import ArgumentParser

from program.common_tool.log_mgr import logger, log_rule, C
from program.common_tool.abstract_entry import AbstractEntry
from program.common_tool.abstract_option_mgr import AbstractOptionMgr
from program.main.helper.option_mgr import option_mgr

class Entry(AbstractEntry):
    @property
    def option_mgr(self) -> AbstractOptionMgr:
        return option_mgr


def main():
    Entry().main()


if __name__ == "__main__":
    main()
