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
        - Market code must be 1-20 characters long.
        - Market code must contain only numbers and uppercase letters.
        - Market code must be in the format of "XXX-XX", where X is a number or uppercase letter.
    Example:
        is_market_valid("ABC-12")  # returns True
        is_market_valid("123-AB")  # returns False"""
    
    p = re.compile(r"^[0-9A-Z]{1,20}\-[1-9A-Z]{2,5}$")
    return p.match(market) is not None


def parse_market(market):
    """Parses a given market into its base currency and quote currency.
    Parameters:
        - market (str): The market to be parsed.
    Returns:
        - market (str): The original market.
        - base_currency (str): The base currency of the market.
        - quote_currency (str): The quote currency of the market.
    Processing Logic:
        - Checks if the given market is valid.
        - Splits the market into its base currency and quote currency.
        - Returns the original market and its base and quote currencies.
    Example:
        market = "BTC-USD"
        parse_market(market)
        # Returns: ("BTC-USD", "BTC", "USD")"""
    
    if not is_market_valid(market):
        raise ValueError(f"Coinbase market invalid: {market}")

    base_currency, quote_currency = market.split("-", 2)
    return market, base_currency, quote_currency


def parser(app, coinbase_config, args={}):
    """This function parses the provided Coinbase configuration and arguments to set up the necessary parameters for the app. It also validates the API key, secret, and URL for Coinbase.
    Parameters:
        - app (object): The app object to be configured.
        - coinbase_config (dict): The configuration for Coinbase, including API key, secret, and URL.
        - args (dict): Additional arguments to be merged with the Coinbase configuration.
    Returns:
        - None: This function does not return any value.
    Processing Logic:
        - Validates the API key and secret for Coinbase.
        - Validates the API URL for Coinbase.
        - Merges the provided arguments with the Coinbase configuration.
        - Sets the base currency and quote currency for the app.
        - Parses the market from the configuration.
        - Sets the granularity for the app."""
    
    if not app:
        raise Exception("No app is passed")

    if isinstance(coinbase_config, dict):
        if "api_key" in coinbase_config or "api_secret" in coinbase_config:
            print(">>> migrating api keys to coinbase.key <<<\n")

            # create 'coinbase.key'
            fh = open("coinbase.key", "w")
            fh.write(f"{coinbase_config['api_key']}\n{coinbase_config['api_secret']}")
            fh.close()

            if os.path.isfile("config.json") and os.path.isfile("coinbase.key"):
                coinbase_config["api_key_file"] = coinbase_config.pop("api_key")
                coinbase_config["api_key_file"] = "coinbase.key"
                del coinbase_config["api_secret"]

                # read 'coinbase' element from config.json
                fh = open("config.json", "r")
                config_json = ast.literal_eval(fh.read())
                config_json["coinbase"] = coinbase_config
                fh.close()

                # write new 'coinbase' element
                fh = open("config.json", "w")
                fh.write(json.dumps(config_json, indent=4))
                fh.close()

        app.api_key_file = "coinbase.key"
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
                    coinbase_config["api_key"] = key
                    coinbase_config["api_secret"] = secret
                except Exception:
                    raise RuntimeError(f"Unable to read {app.api_key_file}")

        if "api_url" in coinbase_config["config"]:
            coinbase_config["api_url"] = coinbase_config["config"]["api_url"]

        if "api_key" in coinbase_config and "api_secret" in coinbase_config and "api_url" in coinbase_config:
            # validates the api key is syntactically correct
            p = re.compile(r"^[A-z0-9]{16,16}$")
            if not p.match(coinbase_config["api_key"]):
                raise TypeError("Coinbase API key is invalid")

            app.api_key = coinbase_config["api_key"]

            # validates the api secret is syntactically correct
            p = re.compile(r"^[A-z0-9]{32,32}$")
            if not p.match(coinbase_config["api_secret"]):
                raise TypeError("Coinbase API secret is invalid")

            app.api_secret = coinbase_config["api_secret"]

            valid_urls = [
                "https://api.coinbase.com/",
                "https://api.coinbase.com",
            ]

            # validate Coinbase API
            if coinbase_config["api_url"] not in valid_urls:
                raise ValueError("Coinbase API URL is invalid")

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
