import os
from pathlib import Path

import rich_click as click

from bob.constants import DEFAULT_BUILDDIR


@click.group
def cli() -> None:
    """The ergonomic Ninja-based build system."""


@cli.command()
@click.option(
    "--builddir",
    help="The directory to put the Bob outputs in.",
    type=click.Path(file_okay=False, path_type=Path),
    default=str(DEFAULT_BUILDDIR),
    show_default=True,
)
@click.option(
    "-f",
    "bobfile",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="The input Bobfile",
    default="Bobfile",
    show_default=True,
)
def build(**kwargs) -> None:
    """Build the given Bob project."""

    from bob.commands.build import build

    build(**kwargs)


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
