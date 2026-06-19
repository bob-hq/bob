import shutil
import subprocess
import sys
from pathlib import Path

from bob.log import console


def completions(shell: str) -> None:
    bob = shutil.which("bob")
    assert bob is not None and Path(bob).resolve() == Path(sys.argv[0]).resolve(), (
        "You must be running a `bob` that is in the PATH to install shell completions!"
    )

    match shell:
        case "fish":
            completions_path = (
                Path.home() / ".config" / "fish" / "completions" / "bob.fish"
            )
            completions_path.parent.mkdir(parents=True, exist_ok=True)
            with open(completions_path, "w") as f:
                subprocess.check_call(
                    f"_BOB_COMPLETE={shell}_source {bob}", stdout=f, shell=True
                )
            console.print(f"Completion script written to {completions_path}")
        case _:
            raise NotImplementedError(f'Completions are not supported for "{shell}"')
