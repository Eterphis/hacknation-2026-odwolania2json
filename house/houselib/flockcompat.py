"""Portable `fcntl.flock` subset, so houselib imports and locks work on Windows too.

Used by: `exp`, `inbox`, `signalagent`, `signalstore` as `from .flockcompat import fcntl`.
On POSIX `fcntl` is the real module. On Windows it is a shim with `flock(fd_or_file, op)` and the
`LOCK_EX`/`LOCK_NB`/`LOCK_UN` constants, built on `msvcrt.locking` over the first byte of the file.
A non-blocking lock that is already held raises `BlockingIOError`, like POSIX.
"""
import os
import sys

if os.name != "nt":
    import fcntl  # noqa: F401
else:
    import msvcrt
    import time
    import types

    LOCK_SH, LOCK_EX, LOCK_NB, LOCK_UN = 1, 2, 4, 8

    def _fd(f) -> int:
        return f if isinstance(f, int) else f.fileno()

    def flock(f, op: int) -> None:
        """Lock or unlock byte 0 of the file; LOCK_SH is treated as exclusive (Windows has no shared mode here)."""
        fd = _fd(f)
        pos = os.lseek(fd, 0, os.SEEK_CUR)
        os.lseek(fd, 0, os.SEEK_SET)
        try:
            if op & LOCK_UN:
                try:
                    msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
                except OSError:
                    pass
                return
            while True:
                try:
                    msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                    return
                except OSError as e:
                    if op & LOCK_NB:
                        raise BlockingIOError(str(e)) from e
                    time.sleep(0.05)
        finally:
            os.lseek(fd, pos, os.SEEK_SET)

    fcntl = types.SimpleNamespace(LOCK_SH=LOCK_SH, LOCK_EX=LOCK_EX, LOCK_NB=LOCK_NB, LOCK_UN=LOCK_UN, flock=flock)
    sys.modules.setdefault("houselib._fcntl_shim", fcntl)  # type: ignore[arg-type]
