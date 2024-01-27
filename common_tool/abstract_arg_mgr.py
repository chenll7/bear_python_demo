from abc import ABC, abstractmethod
from argparse import ArgumentParser

from common_tool.log_mgr import logger

class MyArgumentParserError(Exception): pass

class MyArgumentParser(ArgumentParser):
    def error(self, message):
        logger.info(f'\n{self.format_help()}')
        raise MyArgumentParserError(message)

class AbstractArgMgr(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def add_parses(self, root_parser: MyArgumentParser) -> None:
        pass

    def init(self):
        root_parser = MyArgumentParser(prog='PROGRAM')
        self.add_parses(root_parser)
        self.args = root_parser.parse_args()
        if self.args.subparser_name == None:
            root_parser.print_help()
            raise Exception('Sub-command needed!')
