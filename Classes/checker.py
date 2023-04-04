from bs4 import BeautifulSoup as soup
import logging, configparser, time
import datetime
from Classes.telegram import Telegram
from Sources import sources

# Setting up the config variables

config = configparser.ConfigParser()
config.read("config.ini")

telegram_settings = config["TELEGRAM"]
telegram_chat_id = telegram_settings.get("chat_id")
telegram_token = telegram_settings.get("token")
telegram_disable_notification = telegram_settings.get("disable_notification")

general_settings = config["GENERAL"]
check_delay = general_settings.getint("check_delay")

# Setting up the Products
product_settings = config["PRODUCTS"]
search_query = product_settings.get("product_name")
search_query = search_query.replace('"', "")
price_threshold = product_settings.getfloat("price_threshold")


telegram = Telegram(                                        # You can omit or leave None if you don't want to receive updates on Telegram
    chat_id= telegram_chat_id,                              # Chat ID to send messages @GiveChatId
    token=telegram_token,                                   # Telegram API token @BotFather
    disable_notification=telegram_disable_notification,     # Revoke the notification (sound/vibration)
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

def check_product():    
    # Search for the product in all available sources
    results = sources.search_product(search_query)

    # If no results were found, return None
    if results is None:
        return None
    
    # Sort the results by price
    results.sort(key=lambda x: x["price"])

    # Return the lowest price
    return results, float(results[0]["price"])


def run():
    # Set up the logging
    logging.basicConfig(filename=f'promo_catcher_{datetime.date.today()}.log', level=logging.INFO)


    print(f"Searching for {search_query}")
    while True:
        results, lowest_price = check_product()
        if lowest_price is not None:
            if lowest_price < price_threshold:
                # Send the results to Telegram
                    #telegram.send(f"Lowest price found: R${results[0]['price']} ({results[0]['name']})\n{results[0]['url']}")
                    print(f"Lowest price of the week: {bcolors.OKGREEN}${lowest_price:.2f}{bcolors.ENDC}")
        else:
            print("No product found.")
        print(f"Last checked: {datetime.now()}")
        time.sleep(3600 * 6) # check once a day

run()