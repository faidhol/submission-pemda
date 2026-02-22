import logging
from utils.logger import setup_logger
from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_gsheet, save_to_postgres


def main():
    setup_logger()
    logging.info("===== ETL PIPELINE STARTED =====")

    try:
        # EXTRACT
        raw_data = extract_data()
        logging.info(f"Extracted {len(raw_data)} raw records")

        # TRANSFORM
        clean_data = transform_data(raw_data)
        logging.info(f"Transformed into {len(clean_data)} clean records")

        if clean_data.empty:
            logging.warning("No valid data after transformation")
            return

        # LOAD
        save_to_csv(clean_data)
        save_to_gsheet(clean_data)
        save_to_postgres(clean_data)

        logging.info("===== ETL PIPELINE COMPLETED SUCCESSFULLY =====")

    except Exception as e:
        logging.error(f"ETL Pipeline failed: {e}")


if __name__ == "__main__":
    main()