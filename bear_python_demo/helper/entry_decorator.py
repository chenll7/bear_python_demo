import bear_python_demo as main_package
from bear_python_demo.common_tool.entry_decorator import entry as base_entry
from bear_python_demo.common_tool.config_mgr import ConfigStrategy


def _config_init_additional(config, config_raw):
    pass


def _config_to_json_additional(json):
    pass


def entry():
    return base_entry(
        main_package=main_package,
        config_strategy=ConfigStrategy(
            init_additional=_config_init_additional,
            to_json_additional=_config_to_json_additional
        )
    )
