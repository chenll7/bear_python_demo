from abc import ABC, abstractmethod
import tomllib
from typing import cast, Optional, Type, Generic, TypeVar, Callable
from dataclasses import dataclass, field

from common_tool.log_mgr import logger


class SimpleJsonable:
    def to_json(self):
        j = vars(self).copy()
        return j


@dataclass
class CheckUpdateConfig(SimpleJsonable):
    @dataclass
    class CheckUpdate(SimpleJsonable):
        enabled: bool
        target_dir_path: str

    check_update: CheckUpdate

    def to_json(self):
        j = super().to_json()
        j["check_update"] = self.check_update.to_json()
        return j


@dataclass
class BaseConfig(SimpleJsonable):
    @dataclass
    class General(SimpleJsonable):
        pass

    @dataclass
    class Version(SimpleJsonable):
        version: str

    version: Version
    general: General

    def to_json(self):
        j = super().to_json()
        j["version"] = self.version.to_json()
        j["general"] = self.general.to_json()
        return j


T = TypeVar("T", bound=BaseConfig)


class AbstractConfigMgr(ABC, Generic[T]):
    def __init__(self):
        # 读取配置
        with open("config.toml", "rb") as f:
            self.config_raw = tomllib.load(f)
        self.check_update_config: CheckUpdateConfig | None = None
        self.config: T | None = None

    @property
    @abstractmethod
    def required_config_version(self) -> str:
        pass

    def init_for_check_update(self):
        self.check_update_config = CheckUpdateConfig(
            CheckUpdateConfig.CheckUpdate(
                enabled=self.config_raw["check_update"]["enabled"],
                target_dir_path=self.config_raw["check_update"]["target_dir_path"],
            )
        )

    def init(self):
        # 校验版本
        config_version = self.config_raw["version"]["version"]
        if config_version != self.required_config_version:
            raise Exception(
                f"Configuration file version should be {self.required_config_version} instead of {config_version}"
            )
        logger.info(f"Configuration file version is {self.required_config_version}")
        config_version_frag = BaseConfig.Version(config_version)
        self.config = self.config_factory({"version": config_version_frag})

    @abstractmethod
    def config_factory(self, params_for_base_config) -> T:
        pass
