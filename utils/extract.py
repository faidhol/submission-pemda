import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import logging

BASE_URL = "https://fashion-studio.dicoding.dev"
MAX_RETRY = 3


def build_url(page: int) -> str:
    """Generate correct URL pattern."""
    if page == 1:
        return f"{BASE_URL}/"
    return f"{BASE_URL}/page{page}"


def scrape_page(page: int):
    url = build_url(page)

    for attempt in range(MAX_RETRY):
        try:
            response = requests.get(url, timeout=10)
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
        products = soup.select(".collection-card")

        logging.info(f"Page {page} - Found {len(products)} products")

        for product in products:
            details = product.select_one(".product-details")
            if not details:
                continue

            title_tag = details.select_one("h3.product-title")
            price_tag = details.select_one("span.price")

            if not title_tag or not price_tag:
                continue

            title = title_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)

            # Ambil semua <p>
            p_tags = details.find_all("p")

            rating = ""
            colors = ""
            size = ""
            gender = ""

            for p in p_tags:
                text = p.get_text(strip=True)

                if text.startswith("Rating:"):
                    rating = text
                elif text.startswith("Colors:"):
                    colors = text
                elif text.startswith("Size:"):
                    size = text
                elif text.startswith("Gender:"):
                    gender = text

            data = {
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Colors": colors,
                "Size": size,
                "Gender": gender,
                "timestamp": timestamp
            }

            all_products.append(data)

    logging.info(f"Extracted {len(all_products)} records")
    return all_products