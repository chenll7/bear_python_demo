from typing import cast
from datetime import datetime

from common_tool.abstract_config import AbstractConfig

class Config(AbstractConfig):

    REQUIRED_CONFIG_VERSION = '1'

    def init_additional(self, config_raw):
        self.current_time = datetime.now()

    def to_json_additional(self, json):
        if 'current_time' in json.keys():
            json['current_time'] = cast(
                datetime,
                json['current_time']
            ).isoformat()

config = Config()
