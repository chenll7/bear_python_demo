import time
import traceback

from colorama import Fore

from bear_python_demo.helper.config import config
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
        init_time = env_mgr.init_time
        config_version = config.config_version
        subparser_name = arg_mgr.args.subparser_name

        ####################################
        # 主流程
        ####################################
        log_rule("Main")
        logger.info(
            f"The init time is "
            + C(Fore.YELLOW)
            + str(init_time)
            + C(Fore.RESET)
            + "."
        )
        logger.info(
            f"The config version is "
            + C(Fore.YELLOW)
            + config_version
            + C(Fore.RESET)
            + "."
        )
        logger.info(
            f"The controller name is "
            + C(Fore.YELLOW)
            + str(subparser_name)
            + C(Fore.RESET)
            + "."
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
