import bear_python_demo as main_package
from common_tool.entry_decorator import entry as base_entry
from bear_python_demo.helper.config_mgr import config

def entry():
    return base_entry(
        main_package=main_package,
        custom_config=config
    )
