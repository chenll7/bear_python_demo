import time
import traceback

from colorama import Fore

from bear_python_demo.helper.config_mgr import config_mgr
from bear_python_demo.helper.env_mgr import env_mgr
from bear_python_demo.helper.arg_mgr import arg_mgr
from common_tool.log_mgr import logger, log_rule, C, Color
from common_tool.abstract_controller import AbstractController, MyControllerError


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
        assert env_mgr.env != None
        cwd_path = env_mgr.env.cwd_path
        assert config_mgr.config != None
        test_str = config_mgr.config.general.test_str
        test_num = config_mgr.config.general.test_num
        test_date = config_mgr.config.general.test_date
        subparser_name = arg_mgr.args.subparser_name

        ####################################
        # 主流程
        ####################################
        log_rule("Main")
        logger.info(
            f"The current working directory paht is "
            + C(Fore.YELLOW)
            + cwd_path
            + C(Fore.RESET)
            + " ."
        )
        logger.info(
            f"The test string is "
            + C(Fore.RED)
            + test_str
            + C(Fore.RESET)
            + " ."
        )
        logger.info(
            f"The test number is "
            + C(Fore.CYAN)
            + str(test_num)
            + C(Fore.RESET)
            + " ."
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
