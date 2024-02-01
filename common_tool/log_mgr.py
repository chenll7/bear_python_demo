import logging
from logging import Formatter, LogRecord, Logger
import os
from datetime import datetime
import copy
import json

from colorama import Fore

# str, C
# C, str
# C, C
# C/str, ColoredMsg
# ColoredMsg, C/str
# ColoredMsg, ColoredMsg


class Color:
    pass


class C(str):
    def __add__(self, operand):
        if isinstance(operand, ColoredMsg):
            return operand.__radd__(self)
        else:
            return ColoredMsg(self, operand)

    def __radd__(self, operand):
        if isinstance(operand, ColoredMsg):
            return operand.__add__(self)
        else:
            return ColoredMsg(operand, self)


class ColoredMsg:
    def __init__(self, *frag_tuple):
        self.frag_tuple = frag_tuple

    def __add__(self, operand):
        if isinstance(operand, ColoredMsg):
            return ColoredMsg(*self.frag_tuple, *operand.frag_tuple)
        else:
            return ColoredMsg(*self.frag_tuple, operand)

    def __radd__(self, operand):
        if isinstance(operand, ColoredMsg):
            return ColoredMsg(*operand.frag_tuple, *self.frag_tuple)
        else:
            return ColoredMsg(operand, *self.frag_tuple)


def _init() -> Logger:
    class StreamHandlerFormatter(Formatter):
        def format(self, record: LogRecord):
            record_copy = copy.copy(record)
            if isinstance(record_copy.msg, ColoredMsg):
                record_copy.msg = "".join(record_copy.msg.frag_tuple)
            return super().format(record_copy)

    class FileHandlerFormatter(Formatter):
        def format(self, record: LogRecord):
            record_copy = copy.copy(record)
            if isinstance(record_copy.msg, ColoredMsg):
                record_copy.msg = "".join(
                    tuple(
                        filter(
                            lambda s: not isinstance(s, C), record_copy.msg.frag_tuple
                        )
                    )
                )
            elif isinstance(record_copy.msg, C):
                record_copy.msg = ""
            return super().format(record_copy)

    try:
        os.makedirs("log")
    except FileExistsError as err:
        pass

    FMT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

    file_handler = logging.FileHandler(
        "log/{:%Y-%m-%d}.log".format(datetime.now()), encoding="utf-8"
    )
    file_handler.setFormatter(FileHandlerFormatter(FMT))

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(StreamHandlerFormatter(FMT))

    logging.basicConfig(level=logging.DEBUG, handlers=[stream_handler, file_handler])

    logger = logging.getLogger()

    return logger


def log_rule(name="Utitled"):
    # logger = logging.getLogger()
    logger.info(
        C(Fore.GREEN)
        + "┐\n┌───────────────────────────────────────┘\n│ "
        + C(Fore.RED)
        + f"{name}\n"
        + C(Fore.GREEN)
        + "└──────────────────────────────────────"
        + C(Fore.RESET),
    )


logger = _init()


if __name__ == "__main__":
    # logger = logging.getLogger()
    logger.info(C(Fore.RED) + "1234" + C(Fore.RESET))
    logger.info("dfdfdf")
    log_rule("Summary")
    d = {"1234": "444"}
    logger.info(f"\n{json.dumps(d)}")
    logger.info("\n" + C(Fore.YELLOW) + json.dumps(d) + C(Fore.RESET))
    logger.warning("1234")
    logger.error("3333")
    logger.getChild("huhu").getChild("hihi").info("1234")
