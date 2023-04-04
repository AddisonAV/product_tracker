import logging, yaml, time
import datetime
from Classes.telegram import Telegram
from Sources import sources

# Setting up the config variables
with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

telegram_settings = config["TELEGRAM"]


general_settings = config["GENERAL"]

# Setting up the Products
products = config["PRODUCTS"]


telegram = Telegram(                                        # You can omit or leave None if you don't want to receive updates on Telegram
    chat_id= telegram_settings['chat_id'],                              # Chat ID to send messages @GiveChatId
    token= telegram_settings['token'],                                   # Telegram API token @BotFather
    disable_notification= telegram_settings["disable_notification"],     # Revoke the notification (sound/vibration)
)

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

def check_product(search_query:str):    
    # Search for the product in all available sources
    results = sources.search_product(search_query)

    # If no results were found, return None
    if len(results) < 1:
        return None, None
    
    # Sort the results by price
    results.sort(key=lambda x: x["price"])

    # Return the lowest price
    return results, float(results[0]["price"])


def run():
    # Set up the logging
    logging.basicConfig(filename=f'promo_catcher_{datetime.date.today()}.log', level=logging.INFO)


    while True:
        for product in products:
            product_name = product["name"]
            price_threshold = product["price"]
            print(f"Checking for '{product_name}'")
            logging.info(f"Checking for '{product_name}'")
            results, lowest_price = check_product(product_name)
            if lowest_price is not None:
                if lowest_price < price_threshold:
                    # Send the results to Telegram
                        #telegram.send(f"Lowest price found: R${results[0]['price']} ({results[0]['name']})\n{results[0]['url']}")
                        print(f"Lowest price of the week: {bcolors.OKGREEN}${lowest_price:.2f}{bcolors.ENDC}")
            else:
                print("No product found.")
        #end for
        
        print(f"Last checked: {datetime.datetime.now()}")
        logging.info(f"Last checked: {datetime.datetime.now()}")
        time.sleep(3600 * 6) # check once a day

run()