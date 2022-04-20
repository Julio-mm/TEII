""" Unit tests for teii package """


import os

from pathlib import Path
from pytest import fixture


@fixture(scope='session')
def sandbox_root_path(tmpdir_factory):
    """Create sandbox root directory."""

    tmpdir = tmpdir_factory.mktemp("test")
    assert tmpdir.isdir()
    os.chdir(tmpdir)

    return Path.cwd()
