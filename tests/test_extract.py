from utils.extract import extract_data

def test_extract_structure():
    data = extract_data(current_time="2025")
    assert isinstance(data, list)