import logging
from logging import Formatter, LogRecord, Logger
import os
from datetime import datetime
import copy
import json

from colorama import Fore


class Color(str):
    pass


class C(tuple):
    def __new__(cls, *args):
        return super(C, cls).__new__(cls, tuple(args))


def _init() -> Logger:
    class StreamHandlerFormatter(Formatter):
        def format(self, record: LogRecord):
            record_copy = copy.copy(record)
            if isinstance(record_copy.msg, C):
                record_copy.msg = "".join(record_copy.msg)
            return super().format(record_copy)

    class FileHandlerFormatter(Formatter):
        def format(self, record: LogRecord):
            record_copy = copy.copy(record)
            if isinstance(record_copy.msg, C):
                record_copy.msg = "".join(
                    tuple(filter(lambda s: not isinstance(s, Color), record_copy.msg))
                )
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
        C(
            Color(Fore.GREEN),
            "┐\n┌───────────────────────────────────────┘\n│ ",
            Color(Fore.RED),
            f"{name}\n",
            Color(Fore.GREEN),
            "└──────────────────────────────────────",
            Color(Fore.RESET),
        )
    )


logger = _init()


if __name__ == "__main__":
    # logger = logging.getLogger()
    logger.info(C(Color(Fore.RED), "1234", Color(Fore.RESET)))
    logger.info("dfdfdf")
    log_rule("Summary")
    d = {"1234": "444"}
    logger.info(f"\n{json.dumps(d)}")
    logger.info(C("\n", Color(Fore.YELLOW), json.dumps(d), Color(Fore.RESET)))
    logger.warning("1234")
    logger.error("3333")
    logger.getChild("huhu").getChild("hihi").info("1234")
