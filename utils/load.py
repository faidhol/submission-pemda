import os
import logging
import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine


def save_to_csv(df, filename="products.csv"):
    try:
        if df.empty:
            logging.warning("CSV not saved: DataFrame is empty")
            return

        df.to_csv(filename, index=False)
        logging.info(f"Saved {len(df)} records to CSV")

    except Exception as e:
        logging.error(f"CSV save failed: {e}")


def save_to_gsheet(df, spreadsheet_name="ETL Fashion Data"):
    try:
        if df.empty:
            logging.warning("GSheet not saved: DataFrame is empty")
            return

        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(
            "google-sheets-api.json",
            scopes=scope
        )

        client = gspread.authorize(creds)

        try:
            spreadsheet = client.open(spreadsheet_name)
        except gspread.exceptions.SpreadsheetNotFound:
            spreadsheet = client.create(spreadsheet_name)

        sheet = spreadsheet.sheet1
        sheet.clear()

        sheet.update(
            [df.columns.tolist()] + df.values.tolist()
        )

        logging.info(f"Saved {len(df)} records to Google Sheets")

    except Exception as e:
        logging.error(f"GSheet failed: {e}")


def save_to_postgres(df, table_name="fashion_products"):
    try:
        if df.empty:
            logging.warning("Postgres not saved: DataFrame is empty")
            return

        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL not set")

        engine = create_engine(db_url)

        df.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False
        )

        engine.dispose()

        logging.info(f"Saved {len(df)} records to PostgreSQL")

    except Exception as e:
        logging.error(f"Postgres failed: {e}")