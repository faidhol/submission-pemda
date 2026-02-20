import logging

def setup_logger():
    logging.basicConfig(
        filename="etl.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )