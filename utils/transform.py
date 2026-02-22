import pandas as pd
import logging

EXCHANGE_RATE = 16000


def transform_data(data):
    try:
        df = pd.DataFrame(data)

        if df.empty:
            logging.warning("Empty DataFrame received in transform stage")
            return df

        logging.info(f"Initial records: {len(df)}")

        # ========================
        # PRICE CLEANING
        # ========================
        if "Price" in df.columns:
            df["Price"] = (
                df["Price"]
                .str.replace("$", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip()
            )
            df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
            df["Price"] = df["Price"] * EXCHANGE_RATE

        # ========================
        # RATING CLEANING
        # ========================
        if "Rating" in df.columns:
            df["Rating"] = df["Rating"].str.extract(r"(\d+\.?\d*)")
            df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

        # ========================
        # COLORS CLEANING
        # ========================
        if "Colors" in df.columns:
            df["Colors"] = df["Colors"].str.extract(r"(\d+)")
            df["Colors"] = pd.to_numeric(df["Colors"], errors="coerce")

        # ========================
        # SIZE CLEANING
        # ========================
        if "Size" in df.columns:
            df["Size"] = df["Size"].str.replace("Size: ", "", regex=False)

        # ========================
        # GENDER CLEANING
        # ========================
        if "Gender" in df.columns:
            df["Gender"] = df["Gender"].str.replace("Gender: ", "", regex=False)

        # ========================
        # DATA VALIDATION
        # ========================

        # Drop invalid essential fields only
        df = df.dropna(subset=["Title", "Price"])

        # Remove invalid values
        df = df[df["Price"] > 0]
        df = df[df["Rating"] <= 5]

        # Remove placeholder products
        df = df[df["Title"] != "Unknown Product"]

        # Remove duplicates
        df = df.drop_duplicates()

        logging.info(f"Records after cleaning: {len(df)}")

        # ========================
        # FINAL TYPE ENFORCEMENT
        # ========================
        df = df.astype({
            "Title": "string",
            "Price": "int64",
            "Rating": "float64",
            "Colors": "Int64",
            "Size": "string",
            "Gender": "string"
        })

        return df

    except Exception as e:
        logging.error(f"Transform error: {e}")
        return pd.DataFrame()