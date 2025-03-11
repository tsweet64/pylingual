#!/usr/bin/env python3

import subprocess
import sys
import shlex
import shutil
import py_compile
import functools

from pylingual.utils.version import PythonVersion


class CompileError(Exception):
    success = False
    bc_a = None


@functools.cache
def has_pyenv():
    return shutil.which("pyenv") is not None


def compile_version(py_file, out_file, version):
    py_file = str(py_file)
    out_file = str(out_file)
    version = PythonVersion(version)
    if version == sys.version_info:
        try:
            py_compile.compile(py_file, cfile=out_file, doraise=True, optimize=0)
        except py_compile.PyCompileError as e:
            raise CompileError(str(e))
        return
    compile_cmd = f"import py_compile, sys; assert sys.version_info[:2] == {version.as_tuple()!r}; py_compile.compile({py_file!r}, cfile={out_file!r})"
    cmd = f"env PYENV_VERSION={version.as_str()} PYTHONWARNINGS=ignore pyenv exec python -c {shlex.quote(compile_cmd)}"
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if output.stderr:
        raise CompileError(output.stderr)
