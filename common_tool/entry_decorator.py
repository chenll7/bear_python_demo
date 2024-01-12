import json
from typing import Callable, Any

import colorama

from common_tool import check_update
from common_tool.log_mgr import logger, log_rule
from common_tool.abstract_config import AbstractConfig


def entry(
    *,
    main_package,
    custom_config: AbstractConfig,
    check_update_exit_callback: None|Callable[[],Any] = None
):
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
            custom_config.init_for_check_update()
            logger.info(
                f'\nConfiguration:\n{json.dumps(custom_config.to_json(),indent = 2)}\n'
            )

            ####################################
            # 检查更新
            ####################################
            log_rule('Check Update')
            if custom_config.check_update.enabled:
                check_update.main(
                    main_package=main_package,
                    custom_config=custom_config,
                    exit_callback=check_update_exit_callback
                )

            ####################################
            # 初始化配置
            ####################################
            log_rule('Init Configuration')
            custom_config.init(
                main_package=main_package
            )
            logger.info(
                f'\nConfiguration:\n{json.dumps(custom_config.to_json(), indent = 2)}\n'
            )

            #########################
            # 执行主函数
            #########################
            method(*args, **kwargs)

        return wrap
    return deco
