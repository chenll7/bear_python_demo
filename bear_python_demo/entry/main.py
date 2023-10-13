import atexit
import time

from colorama import Fore

from bear_python_demo.helper.entry_decorator import entry
from bear_python_demo.common_tool import config_mgr
from bear_python_demo.common_tool.log_mgr import logger, log_rule, C, Color


class Summary:
    def __init__(self):
        self.start_time: float = float('nan')
        self.elapsed_time: float = float('nan')
        self.main_process_ends_gracefully: bool = False

    def print(self):
        self.elapsed_time = time.time() - self.start_time
        log_rule("Summary")
        logger.info(C((
            f'\nElapsed time: {self.elapsed_time}s\n',
            'Main process Ends Gracefully: ', *(
                (Color(Fore.GREEN), 'Yes', Color(Fore.RESET))
                if self.main_process_ends_gracefully
                else (Color(Fore.RED), 'No', Color(Fore.RESET))
            )
        )))


@entry()
def main():
    ####################################
    # 初始化
    ####################################
    log_rule('Main')
    summary = Summary()
    summary.start_time = time.time()
    atexit.register(summary.print)

    ####################################
    # 读取配置
    ####################################
    config = config_mgr.get()
    config_version = config.config_version

    ####################################
    # 主流程
    ####################################
    logger.info(C((
        f'Configuration version is ',
        Color(Fore.YELLOW), config_version, Color(Fore.RESET), '.'
    )))
    logger.info(C((
        Color(Fore.GREEN), 'Hello bear python demo!', Color(Fore.RESET)
    )))

    ####################################
    # 结束
    ####################################
    summary.main_process_ends_gracefully = True


if __name__ == '__main__':
    main()
