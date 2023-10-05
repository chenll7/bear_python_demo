from textwrap import dedent
import atexit
import time

from bear_python_demo.util.entry_decorator import entry
from bear_python_demo.util import config_mgr
from bear_python_demo.util.console_mgr import console


class Summary:
    def __init__(self):
        self.elapsed_time: float = float('nan')
        self.main_process_ends_gracefully: bool = False

    def print(self):
        console.rule("Summary")
        console.log(
            dedent(f'''\
                Elapsed time: {self.elapsed_time}s
                Main process Ends Gracefully: {'[green]Yes[/]' if self.main_process_ends_gracefully else '[bold red]No[/]'}\
            ''')
        )


@entry
def main():
    ####################################
    # 初始化
    ####################################
    console.rule('Main')
    summary = Summary()
    atexit.register(summary.print)
    start_time = time.time()

    ####################################
    # 读取配置
    ####################################
    config = config_mgr.get()
    config_version = config.config_version

    ####################################
    # 主流程
    ####################################
    console.log(
        'Configuration version is [yellow]{}[/].'.format(config_version))
    console.log('[green]Hello bear python demo![/]')

    ####################################
    # 结束
    ####################################
    summary.elapsed_time = time.time() - start_time
    summary.main_process_ends_gracefully = True


if __name__ == '__main__':
    main()
