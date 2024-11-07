from quixwrap import Config, Variable


class TestConfig(Config):
    my_secret = Variable("MY_SECRET", qtype="Secret")
    foo = Variable("FOO", default="foo")
    bar = Variable("BAR", default="true", qtype="FreeText")


def test_variable_access():
    assert TestConfig.broker_address == "localhost:19092"
    assert TestConfig.env == "testing"
    assert TestConfig.is_test() is True
    assert TestConfig.is_local() is True


def test_default_parsed():
    assert TestConfig.foo == "foo"


def test_boolean_cast():
    assert TestConfig.bar is True


def test_secret_obfuscated(monkeypatch, capsys):
    monkeypatch.setenv("MY_SECRET", "secret")
    assert TestConfig.my_secret == "secret"
    assert TestConfig.my_secret.text() == "secret"
    print(TestConfig.my_secret)
    out, _ = capsys.readouterr()
    assert "****" in out


def test_app_broker_address(monkeypatch):
    monkeypatch.setenv("Quix__Broker__Address", "kafka:9092")
    assert TestConfig.quix__broker__address == "kafka:9092"
