"""Make sure a `bin/` script runs on Python 3.11+ and, on Windows, in UTF-8 mode.

Used by: every script in `bin/` before it imports anything else from houselib. When the interpreter that started
the script is too old (e.g. `#!/usr/bin/env python3` finds an older python first in PATH) or is a Windows python
without UTF-8 mode (houselib reads and writes Polish UTF-8 text with the default encoding), it re-runs the same
script under a suitable interpreter with `-X utf8` and exits with that run's exit code. stdin/stdout are inherited,
so Claude Code hooks keep working. Keep this file parseable by Python 3.6.
"""
import os
import shutil
import subprocess
import sys

_GUARD = "HOUSE_PYBOOT"
_VERSIONS = ("3.13", "3.12", "3.11", "3.14")


def _works(cmd):
    try:
        return subprocess.call(cmd + ["-c", "import sys; sys.exit(sys.version_info < (3, 11))"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    except OSError:
        return False


def _find_python():
    """Return the command of a Python 3.11+ interpreter, or None."""
    candidates = []
    if os.name == "nt" and shutil.which("py"):
        candidates += [["py", "-" + v] for v in _VERSIONS]
    for v in _VERSIONS:
        exe = shutil.which("python" + v)
        if exe:
            candidates.append([exe])
    for cmd in candidates:
        if _works(cmd):
            return cmd
    return None


def ensure(script):
    """Re-run `script` under Python 3.11+ (UTF-8 mode on Windows) if the current interpreter does not qualify."""
    relaunched = os.environ.pop(_GUARD, None)  # only for this process; child scripts check for themselves
    old = sys.version_info < (3, 11)
    no_utf8 = os.name == "nt" and not sys.flags.utf8_mode
    if not (old or no_utf8):
        return
    if old:
        cmd = None if relaunched else _find_python()
        if cmd is None:
            sys.stderr.write("house: needs Python 3.11+ (this is %s at %s)\n"
                             % (sys.version.split()[0], sys.executable))
            sys.exit(1)
    else:
        cmd = [sys.executable]
    env = dict(os.environ)
    env[_GUARD] = "1"
    try:
        code = subprocess.call(cmd + ["-X", "utf8", str(script)] + sys.argv[1:], env=env)
    except KeyboardInterrupt:
        code = 130
    sys.exit(code)
