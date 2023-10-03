from textwrap import dedent
import atexit

from bear_python_demo.util.entry_decorator import entry
from bear_python_demo.util import config_mgr
from bear_python_demo.util.console_mgr import console
 
class Summary:
    def __init__(self):
        self.main_process_ends_gracefully = False

    def print(self):
        console.rule("Summary")
        console.log(dedent(f'''\
            Main process Ends Gracefully: {'[green]Yes[/]' if self.main_process_ends_gracefully else '[bold red]No[/]'}
        '''))

@entry
def main():
####################################
    # 初始化
    ####################################
    console.rule('Main')
    summary = Summary()
    atexit.register(summary.print)

    ####################################
    # 读取配置
    ####################################
    config = config_mgr.get()
    config_version = config.config_version

    ####################################
    # 主流程
    ####################################
    console.log('Configuration version is [yellow]{}[/].'.format(config_version))
    console.log('[green]Hello bear python demo![/]')

    ####################################
    # 结束
    ####################################
    summary.main_process_ends_gracefully = True

if __name__ == '__main__':
    main()