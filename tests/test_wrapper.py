import os
from pathlib import Path

from quixwrap.codegen import QuixWrap

here = Path(__file__).parent

config_file = here / "quix.yaml"

globals_dict = {}
code = (
    QuixWrap(config_file, os.getenv("YAML_VARIABLES_FILE"))
    .deployment("enricher")
    .as_py(standalone=False)
)
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


def test_quix_broker_address_is_used_when_no_broker_address_var(monkeypatch):
    monkeypatch.setenv("Quix__Broker__Address", "kafka:9092")
    monkeypatch.delenv("BROKER_ADDRESS")
    conf = enricher.app_config()
    assert conf["broker_address"] == "kafka:9092"


def test_broker_address_is_used_when_no_quix_broker_address_var(monkeypatch):
    monkeypatch.setenv("Quix__Broker__Address", "kafka:9092")
    conf = enricher.app_config()
    assert conf["broker_address"] == "localhost:19092"


def test_app_config_non_local(monkeypatch):
    monkeypatch.setenv("ENV", "cloud")
    monkeypatch.setenv("Quix__Sdk__Token", "token")
    assert "quix_sdk_token" in enricher.app_config()
    assert "broker_address" not in enricher.app_config()


def test_placeholder_var_replacement():
    assert enricher.config.label == "DefaultEnricher"
