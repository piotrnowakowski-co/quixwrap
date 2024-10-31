from pathlib import Path

from quixwrap.codegen import QuixWrap

here = Path(__file__).parent

config_file = here / "quix.yaml"

globals_dict = {}
code = QuixWrap(config_file).deployment("enricher").as_py(standalone=False)
exec(code, globals_dict)
enricher = globals_dict["Enricher"]


def test_deployment_wrapper_code(capsys):
    assert enricher.config.env == "testing"
    assert enricher.config.debug is True
    assert enricher.config.foo is None
    assert enricher.config.db_conn == "sqlite:///db.sqlite"
    assert enricher.config.is_local() is True
    assert enricher.config.is_test()
    print(enricher.config.db_conn)
    out, _ = capsys.readouterr()
    assert "****" in out
    assert "db.sqlite" not in out


def test_app_config_local():
    assert "broker_address" in enricher.app_config()
    assert "quix_sdk_token" not in enricher.app_config()


def test_app_config_non_local(monkeypatch):
    monkeypatch.setenv("ENV", "cloud")
    monkeypatch.setenv("Quix__Sdk__Token", "token")
    assert "quix_sdk_token" in enricher.app_config()
    assert "broker_address" not in enricher.app_config()
