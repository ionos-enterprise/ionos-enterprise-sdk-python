import inspect
import os
import sys
import unittest


def get_source_files():
    """Return a list of sources files/directories (to check with flake8/pylint)"""
    scripts = []
    modules = ["examples", "ionosenterprise", "tests"]
    py_files = ["setup.py"]

    files = []
    for code_file in scripts + modules + py_files:
        is_script = code_file in scripts
        if not os.path.exists(code_file):  # pragma: no cover
            # The alternative path is needed for Debian's pybuild
            alternative = os.path.join(os.environ.get("OLDPWD", ""), code_file)
            code_file = alternative if os.path.exists(alternative) else code_file
        if is_script:
            with open(code_file, "rb") as script_file:
                shebang = script_file.readline().decode("utf-8")
            if ((sys.version_info[0] == 3 and "python3" in shebang)
                    or ("python" in shebang and "python3" not in shebang)):
                files.append(code_file)
        else:
            files.append(code_file)
    return files


def unittest_verbosity():
    """Return the verbosity setting of the currently running unittest
    program, or None if none is running.
    """
    frame = inspect.currentframe()
    while frame:
        self = frame.f_locals.get("self")
        if isinstance(self, unittest.TestProgram):
            return self.verbosity
        frame = frame.f_back
    return None  # pragma: no cover
