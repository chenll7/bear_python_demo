from abc import ABC, abstractmethod
import os
from os import path
from typing import cast

from dotenv import load_dotenv

from common_tool.log_mgr import logger


class AbstractEnvMgr(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def init_additional(self):
        pass

    def init(self, main_package):

        # 读取环境变量注入配置
        load_dotenv()

        # 获取配置参数
        self.testing_env: str = os.environ.get("TESTING_ENV", "production")
        self.app_name: str = (
            main_package.__name__ + "-dev"
            if self.testing_env != "production"
            else main_package.__name__
        )
        self.app_data_dir_path: str = path.join(
            cast(str, os.getenv("LOCALAPPDATA")), self.app_name
        )

        self.init_additional()
