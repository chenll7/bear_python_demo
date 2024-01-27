from abc import ABC, abstractmethod
from argparse import ArgumentParser

from common_tool.log_mgr import logger


class AbstractArgMgr(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def add_parses(self, root_parser: ArgumentParser) -> None:
        pass

    def init(self):
        root_parser = ArgumentParser(prog='PROGRAM')
        self.add_parses(root_parser)
        self.args = root_parser.parse_args()
        if self.args.subparser_name == None:
            root_parser.print_help()
            raise Exception('Sub-command needed!')
