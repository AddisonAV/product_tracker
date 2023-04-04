from bs4 import BeautifulSoup as soup
import time, requests, logging
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
        self.source_url = "https://www.pichau.com.br/search?q="

    def search_product(self, search_query):
        try:
            url = search_query.replace(" ", "%20")
            url = f"{self.source_url}{url}"
            logging.info(f"Searching for '{search_query}' in '{url}'")
            page = requests.get(url)
            page_content = soup(page.content, "html.parser")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred while making HTTP request: {e}")
            return []

        products = []
        for product in page_content.find_all('a', attrs={'data-cy':"list-product"}):
            product_name = product.find('h2')
            if not product_name:
                continue
            product_name = product_name.text.strip()

            #checking if product is the same as the search query
            valid_product = True
            search_keys = search_query.lower().split()
            for word in search_keys:
                if not re.search(str(word), product_name.lower()): 
                    valid_product = False
            if not valid_product: 
                continue

            #getting product price        
            product_price = product.find('div', class_="")
            if not product_price:
                continue

            prices = re.findall(r'R?\$\s*[\d,]+(?:\.\d{2})?', 
                                product_price.text.strip())            
            
            if len(prices) == 0:
                continue

            # Getting right price
            price = prices[1] if len(prices) > 2 else prices[0]
            price = price.replace("R$", "").replace(" ", "").replace(",", "")

            #adding product to products
            products.append({
                "name": product_name,
                "price": price,
                "url": "https://www.pichau.com.br" + product["href"]
            })

        return products
