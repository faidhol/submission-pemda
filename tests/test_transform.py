from utils.transform import transform_data

def test_transform_valid():
    sample=[{
        "Title":"Shirt",
        "Price":"$10",
        "Rating":"4.5 / 5",
        "Colors":"3 Colors",
        "Size":"Size: M",
        "Gender":"Gender: Men",
        "timestamp":"2025"
    }]
    df=transform_data(sample)
    assert df["Price"].iloc[0]==160000
    assert df["Rating"].iloc[0]==4.5
    assert df["Colors"].iloc[0]==3