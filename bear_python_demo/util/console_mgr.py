from rich.console import Console

global console
global error_console

console: Console = Console(highlight=False)
console._log_render.omit_repeated_times = False

error_console: Console = Console(stderr=True)
error_console._log_render.omit_repeated_times = False
