import pandas as pd
import logging

EXCHANGE_RATE = 16000

def transform_data(data):
    try:
        df = pd.DataFrame(data)

        if df.empty:
            return df

        # Price
        df["Price"] = (
            df["Price"]
            .str.replace("$","",regex=False)
            .str.replace(",","",regex=False)
            .str.strip()
        )
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce") * EXCHANGE_RATE

        # Rating
        df["Rating"] = df["Rating"].str.extract(r"(\d+\.?\d*)")
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

        # Colors
        df["Colors"] = df["Colors"].str.extract(r"(\d+)")
        df["Colors"] = pd.to_numeric(df["Colors"], errors="coerce")

        # Size
        df["Size"] = df["Size"].str.replace("Size: ","",regex=False)

        # Gender
        df["Gender"] = df["Gender"].str.replace("Gender: ","",regex=False)

        # Drop invalid rows
        df = df.dropna()
        df = df[df["Title"] != "Unknown Product"]
        df = df.drop_duplicates()

        # Final type enforcement
        df = df.astype({
            "Title": "string",
            "Price": "int64",
            "Rating": "float64",
            "Colors": "int64",
            "Size": "string",
            "Gender": "string"
        })

        return df

    except Exception as e:
        logging.error(f"Transform error: {e}")
        return pd.DataFrame()