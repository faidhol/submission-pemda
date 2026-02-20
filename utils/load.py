import os
import logging
import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine

def save_to_csv(df):
    try:
        df.to_csv("products.csv", index=False)
        logging.info("Saved to CSV")
    except Exception as e:
        logging.error(f"CSV save failed: {e}")


def save_to_gsheet(df):
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(
            "google-sheets-api.json", scopes=scope
        )
        client = gspread.authorize(creds)

        try:
            sheet = client.open("ETL Fashion Data").sheet1
        except:
            sheet = client.create("ETL Fashion Data").sheet1

        sheet.clear()
        sheet.update([df.columns.tolist()] + df.values.tolist())
        logging.info("Saved to Google Sheets")

    except Exception as e:
        logging.error(f"GSheet failed: {e}")


def save_to_postgres(df):
    try:
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL not set")

        engine = create_engine(db_url)
        df.to_sql("fashion_products", engine, if_exists="replace", index=False)
        logging.info("Saved to PostgreSQL")

    except Exception as e:
        logging.error(f"Postgres failed: {e}")