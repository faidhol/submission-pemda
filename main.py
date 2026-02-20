from utils.logger import setup_logger
from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_gsheet, save_to_postgres

def main():
    setup_logger()

    raw = extract_data()
    clean = transform_data(raw)

    if clean.empty:
        print("No valid data")
        return

    save_to_csv(clean)
    save_to_gsheet(clean)
    save_to_postgres(clean)

    print("ETL SUCCESS")

if __name__ == "__main__":
    main()

