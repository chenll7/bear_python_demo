import time
import traceback

from colorama import Fore

from program.common_tool.log_mgr import logger, log_rule, C
from program.common_tool.abstract_controller import (
    AbstractController,
    MyControllerError,
)
from program.main.helper.option_mgr import option_mgr


class Summary:
    def __init__(self):
        self.start_time: float = float("nan")
        self.elapsed_time: float = float("nan")
        self.main_process_ends_gracefully: bool = False

    def print(self):
        self.elapsed_time = time.time() - self.start_time
        log_rule("Summary")
        logger.info(
            f"\nElapsed time: {self.elapsed_time}s\n"
            + "Main process Ends Gracefully: "
            + (
                C(Fore.GREEN) + "Yes" + C(Fore.RESET)
                if self.main_process_ends_gracefully
                else C(Fore.RED) + "No" + C(Fore.RESET)
            )
        )


class Main(AbstractController):
    def __init__(self):
        self.summary = Summary()

    def _main(self):
        ####################################
        # 初始化
        ####################################
        log_rule("Starting")
        self.summary.start_time = time.time()

        ####################################
        # 读取配置
        ####################################
        assert option_mgr.config != None
        test_str = option_mgr.config['general']['test_str']
        test_num = option_mgr.config['general']['test_num']
        test_date = option_mgr.config['general']['test_date']

        assert option_mgr.env != None
        cwd_path = option_mgr.env['cwd_path']

        assert option_mgr.args != None
        subparser_name = option_mgr.args.subparser_name

        ####################################
        # 主流程
        ####################################
        log_rule("Main")
        logger.debug(f"Debug info!")
        logger.info(
            f"The current working directory path is "
            + C(Fore.YELLOW)
            + cwd_path
            + C(Fore.RESET)
            + " ."
        )
        logger.info(
            f"The test string is " + C(Fore.RED) + test_str + C(Fore.RESET) + " ."
        )
        logger.info(
            f"The test number is " + C(Fore.CYAN) + str(test_num) + C(Fore.RESET) + " ."
        )
        logger.info(
            f"The test date is "
            + C(Fore.MAGENTA)
            + test_date.isoformat()
            + C(Fore.RESET)
            + " ."
        )
        logger.info(
            f"The controller name is "
            + C(Fore.LIGHTCYAN_EX)
            + str(subparser_name)
            + C(Fore.RESET)
            + " ."
        )
        logger.info(C(Fore.GREEN) + "Hello bear python demo!" + C(Fore.RESET))

    def main(self):
        try:
            self._main()
        except Exception as err:
            logger.error(traceback.format_exc())
            raise MyControllerError(err)
        else:
            self.summary.main_process_ends_gracefully = True
        finally:
            self.summary.print()
