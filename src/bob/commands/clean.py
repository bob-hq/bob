import shutil
from pathlib import Path

from bob.constants import COMPDB_NAME


def _clean(builddir: str):
    if Path(builddir).exists():
        shutil.rmtree(builddir)

    if (
        COMPDB_NAME.is_symlink()
        and Path(builddir).resolve() in COMPDB_NAME.resolve().parents
    ):
        COMPDB_NAME.unlink(missing_ok=True)


def clean(builddir: str):
    _clean(builddir)
