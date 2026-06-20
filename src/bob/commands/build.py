import os
from pathlib import Path

from bob.constants import get_build_ninja_path
from bob.core.configure import configure


def run_ninja(builddir: Path) -> None:
    arguments = [
        "ninja",
        "-f",
        str(get_build_ninja_path(builddir)),
    ]

    os.execvp(arguments[0], arguments)


def build(builddir: Path, bobfile: Path) -> None:
    configure(builddir, bobfile)

    run_ninja(builddir)
