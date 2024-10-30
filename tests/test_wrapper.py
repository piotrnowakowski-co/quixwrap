from pathlib import Path

from quixwrap.codegen import QuixWrap

here = Path(__file__).parent

config_file = here / "quix.yaml"

globals_dict = {}
code = QuixWrap(config_file).deployment("enricher").as_py(standalone=False)
exec(code, globals_dict)


def test_deployment_wrapper_code(capsys):
    enricher = globals_dict["Enricher"]
    assert enricher.config.env == "testing"
    assert enricher.config.debug is True
    assert enricher.config.foo is None
    assert enricher.config.db_conn == "sqlite:///db.sqlite"
    print(enricher.config.db_conn)
    out, _ = capsys.readouterr()
    assert "****" in out
    assert 'db.sqlite' not in out
