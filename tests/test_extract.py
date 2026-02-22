import requests

from utils import extract


def test_scrape_page_success(monkeypatch):
    class FakeResponse:
        text = "<html></html>"

        def raise_for_status(self):
            return None

    monkeypatch.setattr("utils.extract.requests.get", lambda *args, **kwargs: FakeResponse())
    result = extract.scrape_page(1)
    assert result == "<html></html>"


def test_scrape_page_retries_and_returns_none(monkeypatch):
    monkeypatch.setattr(
        "utils.extract.requests.get",
        lambda *args, **kwargs: (_ for _ in ()).throw(requests.RequestException("boom")),
    )
    monkeypatch.setattr("utils.extract.time.sleep", lambda *_args, **_kwargs: None)

    result = extract.scrape_page(1)
    assert result is None


def test_extract_structure_and_timestamp(monkeypatch):
    fake_html = """
    <div class='card'>
      <h3>Casual Shirt</h3>
      <span class='price'>$12.00</span>
      <span class='rating'>4.7 / 5</span>
      <span class='colors'>2 Colors</span>
      <span class='size'>Size: L</span>
      <span class='gender'>Gender: Men</span>
    </div>
    """

    monkeypatch.setattr(extract, "scrape_page", lambda page: fake_html)

    data = extract.extract_data(current_time="2025-01-01T00:00:00")

    assert len(data) == 50
    first = data[0]
    assert first["Title"] == "Casual Shirt"
    assert first["Price"] == "$12.00"
    assert first["Rating"] == "4.7 / 5"
    assert first["Colors"] == "2 Colors"
    assert first["Size"] == "Size: L"
    assert first["Gender"] == "Gender: Men"
    assert first["timestamp"] == "2025-01-01T00:00:00"


def test_extract_skips_invalid_card(monkeypatch):
    valid_html = """
    <div class='card'>
      <h3>Valid Product</h3>
      <span class='price'>$5</span>
      <span class='rating'>4.0 / 5</span>
      <span class='colors'>1 Colors</span>
      <span class='size'>Size: S</span>
      <span class='gender'>Gender: Women</span>
    </div>
    <div class='card'><h3>Broken Product</h3></div>
    """

    monkeypatch.setattr(extract, "scrape_page", lambda page: valid_html if page == 1 else None)

    data = extract.extract_data(current_time="2025")

    assert len(data) == 1
    assert data[0]["Title"] == "Valid Product"