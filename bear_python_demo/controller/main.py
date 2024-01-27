import time

from colorama import Fore

from bear_python_demo.helper.config import config
from bear_python_demo.helper.env_mgr import env_mgr
from bear_python_demo.helper.arg_mgr import arg_mgr
from common_tool.log_mgr import logger, log_rule, C, Color
from common_tool.abstract_controller import AbstractController

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

class Main(AbstractController):
    def __init__(self):
        self.summary = Summary()
        self.summary.start_time = time.time()

    def _main(self):
        ####################################
        # 初始化
        ####################################
        log_rule('Starting')
        self.summary.start_time = time.time()

        ####################################
        # 读取配置
        ####################################
        init_time = env_mgr.init_time
        config_version = config.config_version
        subparser_name = arg_mgr.args.subparser_name

        ####################################
        # 主流程
        ####################################
        log_rule('Main')
        logger.info(C((
            f'The init time is ',
            Color(Fore.YELLOW), str(init_time), Color(Fore.RESET), '.'
        )))
        logger.info(C((
            f'The config version is ',
            Color(Fore.YELLOW), config_version, Color(Fore.RESET), '.'
        )))
        logger.info(C((
            f'The controller name is ',
            Color(Fore.YELLOW), str(subparser_name), Color(Fore.RESET), '.'
        )))
        logger.info(C((
            Color(Fore.GREEN), 'Hello bear python demo!', Color(Fore.RESET)
        )))

    def main(self):
        try:
            self._main()
        except Exception as err:
            raise err
        else:
            self.summary.main_process_ends_gracefully = True
        finally:
            self.summary.print()


