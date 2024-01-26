from argparse import ArgumentParser

import bear_python_demo as main_package
from bear_python_demo.helper.config_mgr import config
from common_tool.log_mgr import logger, log_rule, C, Color
from common_tool.abstract_entry import AbstractEntry

class Entry(AbstractEntry):
    @property
    def main_package(self):
        return main_package

    @property
    def custom_config(self):
        return config
    
    def add_parses(self, root_parser: ArgumentParser) -> None:
        subparsers = root_parser.add_subparsers(dest='subparser_name', help='Sub-command.')
        main_parser = subparsers.add_parser('main', help='Main.')

def main():
    Entry().main()

if __name__ == "__main__":
    main()
