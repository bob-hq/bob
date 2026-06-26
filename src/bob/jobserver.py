import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import bob.external.job_server_pool as job_server_pool


@contextmanager
def jobserver(jobs: int) -> Generator[None, None, None]:
    if jobs <= 0:
        raise ValueError("Cannot run a jobserver with non-positive jobs!")

    if job_server_pool._IS_WINDOWS:  # type: ignore[attr-defined]
        # Run with a Window semaphore.
        try:
            handle, env = job_server_pool.create_sem(  # type: ignore[attr-defined]
                job_server_pool._DEFAULT_NAME,  # type: ignore[attr-defined]
                jobs,
            )
            os.environ["MAKEFLAGS"] = env["MAKEFLAGS"]
            yield
        finally:
            os.environ.pop("MAKEFLAGS")
            job_server_pool.win32api.CloseHandle(handle)  # type: ignore[attr-defined]
    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            fifo_path = tmpdir_path / "jobserver"

            read_fd = None
            write_fd = None
            try:
                read_fd, write_fd, env = job_server_pool.create_fifo(  # type: ignore[attr-defined]
                    str(fifo_path), jobs
                )
                os.environ["MAKEFLAGS"] = env["MAKEFLAGS"]
                yield
            finally:
                os.environ.pop("MAKEFLAGS")
                if read_fd is not None:
                    os.close(read_fd)
                if write_fd is not None:
                    os.close(write_fd)
                os.remove(fifo_path)
