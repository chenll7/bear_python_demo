from abc import ABC, abstractmethod
import os
from os import path
from typing import cast, TypeVar, Generic
from dataclasses import dataclass

from dotenv import load_dotenv

from common_tool.log_mgr import logger
from common_tool.util import SimpleJsonable


@dataclass
class BaseEnv(SimpleJsonable):
    testing_env: str
    app_name: str
    app_data_dir_path: str


T = TypeVar("T", bound=BaseEnv)


class AbstractEnvMgr(ABC, Generic[T]):
    def __init__(self):
        self.env: T | None = None

    def init(self, main_package):
        # 读取环境变量注入配置
        load_dotenv()

        testing_env = os.environ.get("TESTING_ENV", "production")
        app_name = (
            main_package.__name__ + "-dev"
            if testing_env != "production"
            else main_package.__name__
        )
        self.env = self.env_factory(
            {
                "testing_env": testing_env,
                "app_name": app_name,
                "app_data_dir_path": path.join(
                    cast(str, os.getenv("LOCALAPPDATA")), app_name
                ),
            }
        )

    @abstractmethod
    def env_factory(self, params_for_env) -> T:
        pass
