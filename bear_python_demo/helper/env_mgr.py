from typing import cast
from datetime import datetime

from common_tool.abstract_env_mgr import AbstractEnvMgr

class EnvMgr(AbstractEnvMgr):
    def init_additional(self):
        self.init_time = datetime.now()

env_mgr = EnvMgr()
