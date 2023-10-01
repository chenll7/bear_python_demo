from bear_python_demo.util import config_mgr
from bear_python_demo.util import check_update

from bear_python_demo.util.console_mgr import console


def entry(method):
    def wrap():
        ####################################
        # 初始化配置
        ####################################
        console.rule('Init Configuration')
        config_mgr.init()
        config = config_mgr.get()
        console.log('Configuration:', config.to_json(), "", highlight=True)

        ####################################
        # 检查更新
        ####################################
        console.rule('Check Update')
        if config.check_update.enabled:
            check_update.main()

        #########################
        # 执行主函数
        #########################
        method()

    return wrap
