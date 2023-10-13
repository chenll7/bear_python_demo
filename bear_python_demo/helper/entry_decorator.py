from datetime import datetime
from typing import cast

import bear_python_demo as main_package
from bear_python_demo.common_tool.entry_decorator import entry as base_entry
from bear_python_demo.common_tool.config_mgr import Config


class MyConfig(Config):
    def init_additional(self, config_raw):
        self.current_time = datetime.now()

    def to_json_additional(self, json):
        if 'current_time' in json.keys():
            json['current_time'] = cast(
                datetime,
                json['current_time']
            ).isoformat()


def entry():
    return base_entry(
        main_package=main_package,
        custom_config=MyConfig()
    )
