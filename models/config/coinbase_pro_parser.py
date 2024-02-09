import ast
import json
import os.path
import re
import sys

from .default_parser import is_currency_valid, default_config_parse, merge_config_and_args
from models.exchange.Granularity import Granularity


def is_market_valid(market) -> bool:
    """Checks if the given market code is valid.
    Parameters:
        - market (str): The market code to be checked.
    Returns:
        - bool: True if the market code is valid, False otherwise.
    Processing Logic:
        - Uses regular expression to validate market code.
        - Market code must contain 1-20 alphanumeric characters, followed by a hyphen, followed by 2-5 alphanumeric characters.
        - Returns True if the market code matches the pattern, False otherwise."""
    
    p = re.compile(r"^[0-9A-Z]{1,20}\-[1-9A-Z]{2,5}$")
    return p.match(market) is not None


def parse_market(market):
    """"Parses a Coinbase Pro market into its base and quote currencies."
    Parameters:
        - market (str): A Coinbase Pro market in the format of "base_currency-quote_currency".
    Returns:
        - market (str): The original market input.
        - base_currency (str): The base currency of the market.
        - quote_currency (str): The quote currency of the market.
    Processing Logic:
        - Checks if the market is valid.
        - Splits the market into base and quote currencies.
        - Returns the original market input and the base and quote currencies.
    Example:
        parse_market("BTC-USD")
        # Returns ("BTC-USD", "BTC", "USD")"""
    
    if not is_market_valid(market):
        raise ValueError(f"Coinbase Pro market invalid: {market}")

    base_currency, quote_currency = market.split("-", 2)
    return market, base_currency, quote_currency


def parser(app, coinbase_config, args={}):
    """This function is used to parse and migrate API keys from a config file to a new file.
    Parameters:
        - app (object): The application object.
        - coinbase_config (dict): A dictionary containing the API keys and URL.
        - args (dict): Optional dictionary containing additional arguments.
    Returns:
        - None: This function does not return any value.
    Processing Logic:
        - Checks if an app object is passed.
        - Checks if the coinbase_config is a dictionary.
        - Checks if the coinbase_config contains the necessary API keys.
        - Creates a new file and writes the API keys to it.
        - Updates the config file with the new API key file location.
        - Sets the app's API key file.
        - Checks if an API key file is specified in the args or config.
        - Reads the API key file and updates the coinbase_config.
        - Validates the API key, secret, and passphrase.
        - Validates the API URL.
        - Merges the config and args dictionaries.
        - Parses the default config.
        - Sets the app's base and quote currencies.
        - Parses the market from the config.
        - Sets the app's market.
        - Sets the app's granularity."""
    
    if not app:
        raise Exception("No app is passed")

    if isinstance(coinbase_config, dict):
        if "api_key" in coinbase_config or "api_secret" in coinbase_config or "api_passphrase" in coinbase_config:
            print(">>> migrating api keys to coinbasepro.key <<<\n")

            # create 'coinbasepro.key'
            fh = open("coinbasepro.key", "w")
            fh.write(f"{coinbase_config['api_key']}\n{coinbase_config['api_secret']}\n{coinbase_config['api_passphrase']}")
            fh.close()

            if os.path.isfile("config.json") and os.path.isfile("coinbasepro.key"):
                coinbase_config["api_key_file"] = coinbase_config.pop("api_key")
                coinbase_config["api_key_file"] = "coinbasepro.key"
                del coinbase_config["api_secret"]
                del coinbase_config["api_passphrase"]

                # read 'coinbasepro' element from config.json
                fh = open("config.json", "r")
                config_json = ast.literal_eval(fh.read())
                config_json["coinbasepro"] = coinbase_config
                fh.close()

                # write new 'coinbasepro' element
                fh = open("config.json", "w")
                fh.write(json.dumps(config_json, indent=4))
                fh.close()

        app.api_key_file = "coinbasepro.key"
        if "api_key_file" in args and args["api_key_file"] is not None:
            app.api_key_file = args["api_key_file"]
        elif "api_key_file" in coinbase_config:
            app.api_key_file = coinbase_config["api_key_file"]

        if app.api_key_file is not None:
            if not os.path.isfile(app.api_key_file):
                try:
                    raise Exception(f"Unable to read {app.api_key_file}, please check the file exists and is readable. Remove \"api_key_file\" key from the config file for test mode!\n")
                except Exception as e:
                    print(f"{type(e).__name__}: {e}")
                    sys.exit(1)
            else:
                try:
                    with open(app.api_key_file, "r") as f:
                        key = f.readline(5_000_000).strip()
                        secret = f.readline(5_000_000).strip()
                        password = f.readline(5_000_000).strip()
                    coinbase_config["api_key"] = key
                    coinbase_config["api_secret"] = secret
                    coinbase_config["api_passphrase"] = password
                except Exception:
                    raise RuntimeError(f"Unable to read {app.api_key_file}")

        if "api_key" in coinbase_config and "api_secret" in coinbase_config and "api_passphrase" in coinbase_config and "api_url" in coinbase_config:

            # validates the api key is syntactically correct
            p = re.compile(r"^[a-f0-9]{32}$")
            if not p.match(coinbase_config["api_key"]):
                raise TypeError("Coinbase Pro API key is invalid")

            app.api_key = coinbase_config["api_key"]

            # validates the api secret is syntactically correct
            p = re.compile(r"^[A-z0-9+\/]+==$")
            if not p.match(coinbase_config["api_secret"]):
                raise TypeError("Coinbase Pro API secret is invalid")

            app.api_secret = coinbase_config["api_secret"]

            # validates the api passphrase is syntactically correct
            p = re.compile(r"^[A-z0-9#$%=@!{},`~&*()<>?.:;_|^/+\[\]]{8,32}$")
            if not p.match(coinbase_config["api_passphrase"]):
                raise TypeError("Coinbase Pro API passphrase is invalid")

            app.api_passphrase = coinbase_config["api_passphrase"]

            valid_urls = [
                "https://api.exchange.coinbase.com",
                "https://api.exchange.coinbase.com/",
                "https://public.sandbox.pro.coinbase.com",
                "https://public.sandbox.pro.coinbase.com/",
            ]

            # validate Coinbase Pro API
            if coinbase_config["api_url"] not in valid_urls:
                raise ValueError("Coinbase Pro API URL is invalid")

            app.api_url = coinbase_config["api_url"]
    else:
        coinbase_config = {}

    config = merge_config_and_args(coinbase_config, args)

    default_config_parse(app, config)

    if "base_currency" in config and config["base_currency"] is not None:
        if not is_currency_valid(config["base_currency"]):
            raise TypeError("Base currency is invalid.")
        app.base_currency = config["base_currency"]

    if "quote_currency" in config and config["quote_currency"] is not None:
        if not is_currency_valid(config["quote_currency"]):
            raise TypeError("Quote currency is invalid.")
        app.quote_currency = config["quote_currency"]

    if "market" in config and config["market"] is not None:
        app.market, app.base_currency, app.quote_currency = parse_market(config["market"])

    if app.base_currency != "" and app.quote_currency != "":
        app.market = app.base_currency + "-" + app.quote_currency

    if "granularity" in config and config["granularity"] is not None:
        if isinstance(config["granularity"], str) and config["granularity"].isnumeric() is True:
            app.granularity = Granularity.convert_to_enum(int(config["granularity"]))
        elif isinstance(config["granularity"], int):
            app.granularity = Granularity.convert_to_enum(config["granularity"])
