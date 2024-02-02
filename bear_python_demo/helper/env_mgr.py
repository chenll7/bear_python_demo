from typing import cast
from datetime import datetime
from dataclasses import dataclass
import os

from common_tool.abstract_env_mgr import AbstractEnvMgr, BaseEnv
from common_tool.util import SimpleJsonable


@dataclass
class Env(BaseEnv):
    cwd_path: str


class EnvMgr(AbstractEnvMgr[Env]):
    def env_factory(self, params_for_base_env) -> Env:
        return Env(cwd_path=os.getcwd(), **params_for_base_env)


env_mgr = EnvMgr()
