import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import logging

BASE_URL = "https://fashion-studio.dicoding.dev/"
MAX_RETRY = 3

def scrape_page(page: int):
    for attempt in range(MAX_RETRY):
        try:
            response = requests.get(f"{BASE_URL}?page={page}", timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.warning(f"Retry {attempt+1} page {page} failed: {e}")
            time.sleep(1)
    logging.error(f"Failed scraping page {page}")
    return None


def extract_data(current_time=None):
    all_products = []
    timestamp = current_time or datetime.now()

    for page in range(1, 51):
        html = scrape_page(page)
        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")
        products = soup.select(".card")

        for product in products:
            try:
                data = {
                    "Title": product.find("h3").get_text(strip=True),
                    "Price": product.find("span", class_="price").get_text(strip=True),
                    "Rating": product.find("span", class_="rating").get_text(strip=True),
                    "Colors": product.find("span", class_="colors").get_text(strip=True),
                    "Size": product.find("span", class_="size").get_text(strip=True),
                    "Gender": product.find("span", class_="gender").get_text(strip=True),
                    "timestamp": timestamp
                }
                all_products.append(data)
            except AttributeError:
                logging.warning("Missing attribute in product block")
                continue

    logging.info(f"Extracted {len(all_products)} records")
    return all_products