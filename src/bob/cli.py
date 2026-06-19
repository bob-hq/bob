import os
from pathlib import Path

import rich_click as click


@click.group
def cli() -> None:
    """The ergonomic Ninja-based build system."""


@cli.command()
def build() -> None:
    """Build the given Bob project."""


@cli.command
@click.option(
    "--shell",
    help="The shell to install completions for.",
    default=Path(os.environ["SHELL"]).name if "SHELL" in os.environ else None,
    show_default=True,
)
def completions(**kwargs) -> None:
    """Install shell completions for Bob."""

    from bob.commands.completions import completions

    completions(**kwargs)
