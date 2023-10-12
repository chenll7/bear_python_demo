import json

import colorama

from . import config_mgr
from . import check_update
from .log_mgr import logger, log_rule


def entry(*, main_package):
    def deco(method):
        def wrap(*args, **kwargs):
            ####################################
            # 初始化
            ####################################
            colorama.init()

            ####################################
            # 初始化配置，仅检查更新部分
            ####################################
            log_rule('Init Configuration For Check Update')
            config_mgr.init_for_check_update()
            config = config_mgr.get()
            logger.info(
                f'\nConfiguration:\n{json.dumps(config.to_json(),indent = 2)}\n'
            )

            ####################################
            # 检查更新
            ####################################
            log_rule('Check Update')
            if config.check_update.enabled:
                check_update.main(main_package=main_package)

            ####################################
            # 初始化配置
            ####################################
            log_rule('Init Configuration')
            config_mgr.init(
                main_package=main_package
            )
            config = config_mgr.get()
            logger.info(
                f'\nConfiguration:\n{json.dumps(config.to_json(),indent = 2)}\n'
            )

            #########################
            # 执行主函数
            #########################
            method(*args, **kwargs)

        return wrap
    return deco
