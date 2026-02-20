from utils.logger import setup_logger


def test_setup_logger_calls_basic_config(monkeypatch):
    called = {}

    def fake_basic_config(**kwargs):
        called.update(kwargs)

    monkeypatch.setattr("utils.logger.logging.basicConfig", fake_basic_config)

    setup_logger()

    assert called["filename"] == "etl.log"
    assert called["level"] == 20
    assert "%(asctime)s" in called["format"]