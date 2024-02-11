from dataclasses import dataclass
from datetime import date

from common_tool.abstract_config_mgr import (
    AbstractConfigMgr,
    BaseConfig,
    SimpleJsonable,
)


@dataclass
class Config(BaseConfig):
    @dataclass
    class General(SimpleJsonable):
        test_str: str
        test_num: int
        test_date: date

        def to_json(self):
            j = super().to_json()
            j["test_date"] = self.test_date.isoformat() if self.test_date else None
            return j

    general: General

    def to_json(self):
        j = super().to_json()
        j["general"] = self.general.to_json()
        return j


class ConfigMgr(AbstractConfigMgr[Config]):
    @property
    def required_config_version(self) -> str:
        return "1"

    def config_factory(self, params_for_config) -> Config:
        params_for_config["general"] = Config.General(
            test_str=self.config_raw["general"]["test_str"],
            test_num=self.config_raw["general"]["test_num"],
            test_date=self.config_raw["general"]["test_date"],
        )
        return Config(**params_for_config)


config_mgr = ConfigMgr()
