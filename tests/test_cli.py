import os
import subprocess

env = os.environ.copy()

def execute_cmd(command: str):
    p = subprocess.Popen(command.split(" "), env=env)
    return p.wait()


def test_apps_list():
    res = execute_cmd("quixwrap apps list")
    assert res == 0


def test_apps_list_expand():
    res = execute_cmd("quixwrap apps list --expand")
    assert res == 0


def test_apps_get():
    res = execute_cmd("quixwrap apps get enricher")
    assert res == 0


def test_apps_get_as_py():
    res = execute_cmd("quixwrap apps get enricher --as-py")
    assert res == 0


def test_apps_get_exits_clean_if_app_does_not_exists():
    res = execute_cmd("quixwrap apps get foo")
    assert res == 0
