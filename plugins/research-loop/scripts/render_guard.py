#!/usr/bin/env python3
"""Run one trusted local Python render with a wall timeout and limited threads.

This is a cooperative launcher, not a sandbox or an operating-system CPU/RAM
quota. Direct Python imports do not inherit its timeout or process lock.
"""

import argparse
from contextlib import contextmanager
import getpass
import hashlib
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile

DEFAULT_TIMEOUT = 60
MAX_TIMEOUT = 120
THREAD_VARIABLES = (
    "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS",
)


class RenderLimitError(ValueError):
    pass


def file_metadata(path):
    digest, size = hashlib.sha256(), 0
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(64 * 1024), b""):
            size += len(chunk)
            digest.update(chunk)
    return {"byteSize": size, "sha256": digest.hexdigest()}


@contextmanager
def render_lock():
    """Fail fast if this user's guarded renderer is already running."""
    identity = str(os.getuid()) if hasattr(os, "getuid") else getpass.getuser()
    suffix = hashlib.sha256(identity.encode()).hexdigest()[:16]
    directory = Path(tempfile.gettempdir()) / f"research-loop-render-{suffix}"
    directory.mkdir(mode=0o700, exist_ok=True)
    if directory.is_symlink() or not directory.is_dir():
        raise RenderLimitError("Render lock directory is not a regular directory")
    if hasattr(os, "getuid") and directory.stat().st_uid != os.getuid():
        raise RenderLimitError("Render lock directory belongs to another user")
    lock_path = directory / "active.lock"
    descriptor = os.open(lock_path, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(descriptor, "r+b") as stream:
        locked = False
        try:
            if os.name == "nt":
                import msvcrt
                if lock_path.stat().st_size == 0:
                    stream.write(b"0")
                    stream.flush()
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            locked = True
        except OSError as error:
            raise RenderLimitError("Another Research Loop render is running; wait for it before retrying") from error
        try:
            yield
        finally:
            if locked:
                if os.name == "nt":
                    stream.seek(0)
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(stream, fcntl.LOCK_UN)


def run_python(script, arguments=(), *, timeout=DEFAULT_TIMEOUT):
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not 0 < timeout <= MAX_TIMEOUT:
        raise RenderLimitError(f"Render timeout must be greater than 0 and at most {MAX_TIMEOUT} seconds")
    environment = os.environ.copy()
    environment.update({key: "1" for key in THREAD_VARIABLES})
    environment["MPLBACKEND"] = "Agg"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    with render_lock():
        process = subprocess.Popen(
            [sys.executable, str(script), *map(str, arguments)], env=environment,
            start_new_session=os.name != "nt",
        )
        try:
            return process.wait(timeout=timeout)
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
            if os.name != "nt":
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                process.kill()
            process.wait()
            if isinstance(error, KeyboardInterrupt):
                raise
            raise RenderLimitError(f"Render exceeded {timeout:g} seconds and was stopped; simplify the figure") from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("script", type=Path)
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    try:
        return run_python(args.script, args.arguments, timeout=args.timeout)
    except (RenderLimitError, OSError) as error:
        print(f"render-guard: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
