import json

from bear_python_demo.util import config_mgr
from bear_python_demo.util import check_update

from bear_python_demo.util.log_mgr import logger, log_rule


def entry(method):
    def wrap(*args, **kwargs):
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
            check_update.main()

        ####################################
        # 初始化配置
        ####################################
        log_rule('Init Configuration')
        config_mgr.init()
        config = config_mgr.get()
        logger.info(
            f'\nConfiguration:\n{json.dumps(config.to_json(),indent = 2)}\n'
        )

        #########################
        # 执行主函数
        #########################
        method(*args, **kwargs)

    return wrap
