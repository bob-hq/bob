from pathlib import Path

from bob.constants import get_build_ninja_path
from bob.core.context import Context


def configure(builddir: Path, bobfile: Path) -> None:
    build_ninja_path = get_build_ninja_path(builddir)

    build_ninja_path.parent.mkdir(parents=True, exist_ok=True)

    with Context(builddir) as context:
        context.evaluate(bobfile)
