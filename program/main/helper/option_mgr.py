import os

from program.common_tool.abstract_option_mgr import AbstractOptionMgr, MyArgumentParser


class ConfigMgr(AbstractOptionMgr):
    @property
    def required_config_version(self) -> str:
        return "1"

    def add_env(self) -> None:
        assert isinstance(self.env, dict)
        self.env["cwd_path"] = os.getcwd()

    def add_parses(self, root_parser: MyArgumentParser) -> None:
        subparsers = root_parser.add_subparsers(
            dest="subparser_name", help="Sub-command."
        )
        main_parser = subparsers.add_parser("main", help="Main.")


option_mgr = ConfigMgr()
