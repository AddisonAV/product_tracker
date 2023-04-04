from bs4 import BeautifulSoup as soup
import requests
import logging
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class pichau:
    def __init__(self):
        self.search_url = "https://www.pichau.com.br/search?q="

    def search_product(self, search_query):
        try:
            search_url = f"{self.search_url}{search_query.replace(' ', '%20')}"
            logging.info(f"Searching for '{search_query}' in '{search_url}'")
            page = requests.get(search_url)
            page_soup = soup(page.content, "html.parser")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred while making HTTP request: {e}")
            return []

        products = []
        for product in page_soup.find_all('a', attrs={'data-cy': 'list-product'}):
            product_name = product.find('h2')
            if not product_name:
                continue
            product_name = product_name.text.strip()

            # Check if product name matches search query
            matches_query = all(word in product_name.lower() for word in search_query.lower().split())
            if not matches_query:
                continue

            # Get product price
            product_price = product.find('div', class_="")
            if not product_price:
                continue
            price_matches = re.findall(r'R?\$\s*[\d,]+(?:\.\d{2})?', product_price.text.strip())
            if not price_matches:
                continue
            price = price_matches[1] if len(price_matches) > 1 else price_matches[0]
            price = price.replace("R$", "").replace(" ", "").replace(",", "")

            # Add product to list
            products.append({
                "name": product_name,
                "price": price,
                "url": f"https://www.pichau.com.br{product['href']}"
            })

        return products
