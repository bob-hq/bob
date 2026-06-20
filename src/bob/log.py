import logging
import runpy

import click
import rich_click
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install as rich_traceback_install

import bob

console = Console()


def setup() -> None:
    rich_traceback_install(console=console, suppress=[click, rich_click, bob, runpy])

    logging.basicConfig(
        level=logging.WARNING,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(show_time=False)],
    )
