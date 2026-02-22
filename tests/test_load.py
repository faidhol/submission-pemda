from pathlib import Path

import pandas as pd

from utils.load import save_to_csv, save_to_gsheet, save_to_postgres


def test_save_csv_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    df = pd.DataFrame({"A": [1], "B": ["x"]})

    save_to_csv(df)

    out = Path("products.csv")
    assert out.exists()
    written = pd.read_csv(out)
    assert written.shape == (1, 2)


def test_save_to_gsheet_happy_path(monkeypatch):
    class FakeSheet:
        def clear(self):
            self.cleared = True

        def update(self, values):
            self.updated = values

    class FakeClient:
        def __init__(self):
            self.sheet = FakeSheet()

        def open(self, _):
            return type("Book", (), {"sheet1": self.sheet})

    monkeypatch.setattr("utils.load.Credentials.from_service_account_file", lambda *_args, **_kwargs: object())
    monkeypatch.setattr("utils.load.gspread.authorize", lambda _creds: FakeClient())

    df = pd.DataFrame({"Title": ["A"], "Price": [100]})
    save_to_gsheet(df)


def test_save_to_postgres_uses_engine(monkeypatch):
    df = pd.DataFrame({"Title": ["A"], "Price": [100]})
    called = {}

    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")

    def fake_create_engine(url):
        called["url"] = url
        return "engine"

    def fake_to_sql(self, name, engine, if_exists, index):
        called["name"] = name
        called["engine"] = engine
        called["if_exists"] = if_exists
        called["index"] = index

    monkeypatch.setattr("utils.load.create_engine", fake_create_engine)
    monkeypatch.setattr(pd.DataFrame, "to_sql", fake_to_sql, raising=True)

    save_to_postgres(df)

    assert called["url"].startswith("postgresql://")
    assert called["name"] == "fashion_products"
    assert called["engine"] == "engine"
    assert called["if_exists"] == "replace"
    assert called["index"] is False


def test_save_to_postgres_without_database_url_does_not_raise(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    df = pd.DataFrame({"A": [1]})

    save_to_postgres(df)