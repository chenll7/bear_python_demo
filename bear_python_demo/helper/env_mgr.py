from dataclasses import dataclass
import os

from common_tool.abstract_env_mgr import AbstractEnvMgr, BaseEnv


@dataclass
class Env(BaseEnv):
    cwd_path: str


class EnvMgr(AbstractEnvMgr[Env]):
    def env_factory(self, params_for_env) -> Env:
        params_for_env["cwd_path"] = os.getcwd()
        return Env(**params_for_env)


env_mgr = EnvMgr()
