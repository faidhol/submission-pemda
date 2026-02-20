from utils.transform import transform_data

def test_transform_valid_data_and_types():
    sample = [
        {
            "Title": "Shirt",
            "Price": "$10",
            "Rating": "4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2025",
        }
    ]

    df = transform_data(sample)

    assert df["Price"].iloc[0] == 160000
    assert df["Rating"].iloc[0] == 4.5
    assert df["Colors"].iloc[0] == 3
    assert df["Size"].iloc[0] == "M"
    assert df["Gender"].iloc[0] == "Men"
    assert str(df["Price"].dtype) == "int64"
    assert str(df["Rating"].dtype) == "float64"


def test_transform_drops_invalid_null_and_duplicate_rows():
    sample = [
        {
            "Title": "Unknown Product",
            "Price": "$10",
            "Rating": "4.0 / 5",
            "Colors": "2 Colors",
            "Size": "Size: L",
            "Gender": "Gender: Men",
            "timestamp": "2025",
        },
        {
            "Title": "Good Product",
            "Price": "$20",
            "Rating": "4.8 / 5",
            "Colors": "4 Colors",
            "Size": "Size: XL",
            "Gender": "Gender: Women",
            "timestamp": "2025",
        },
        {
            "Title": "Good Product",
            "Price": "$20",
            "Rating": "4.8 / 5",
            "Colors": "4 Colors",
            "Size": "Size: XL",
            "Gender": "Gender: Women",
            "timestamp": "2025",
        },
        {
            "Title": "Bad Price",
            "Price": "not-a-price",
            "Rating": "4.2 / 5",
            "Colors": "2 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2025",
        },
    ]

    df = transform_data(sample)

    assert len(df) == 1
    assert df["Title"].iloc[0] == "Good Product"


def test_transform_returns_empty_for_invalid_payload_type():
    df = transform_data("not-a-list")
    assert df.empty