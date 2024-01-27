from common_tool.abstract_arg_mgr import AbstractArgMgr, MyArgumentParser

class ArgMgr(AbstractArgMgr):
    def add_parses(self, root_parser: MyArgumentParser) -> None:
        subparsers = root_parser.add_subparsers(dest='subparser_name', help='Sub-command.')
        main_parser = subparsers.add_parser('main', help='Main.')

arg_mgr = ArgMgr()
