import re
import ast
import json
import os.path
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
        - Uses regular expression to validate the market code.
        - Market code must contain 1-20 alphanumeric characters, followed by a hyphen, followed by 2-5 alphanumeric characters.
        - Returns True if the market code matches the pattern, False otherwise."""
    
    p = re.compile(r"^[0-9A-Z]{1,20}\-[1-9A-Z]{2,5}$")
    return p.match(market) is not None


def parse_market(market):
    """Parses a Kucoin market string into its base currency and quote currency components.
    Parameters:
        - market (str): The Kucoin market string to be parsed.
    Returns:
        - market (str): The original market string.
        - base_currency (str): The base currency component of the market.
        - quote_currency (str): The quote currency component of the market.
    Processing Logic:
        - Checks if the market string is valid.
        - Splits the market string into base and quote currencies.
        - Returns the original market string and its components.
    Example:
        parse_market("ETH-BTC")
        # Returns ("ETH-BTC", "ETH", "BTC")"""
    
    if not is_market_valid(market):
        raise ValueError("Kucoin market invalid: " + market)

    base_currency, quote_currency = market.split("-", 2)
    return market, base_currency, quote_currency


def parser(app, kucoin_config, args={}):
    """        else:
                raise TypeError("Granularity is invalid.")
        if "start_date" in config and config["start_date"] is not None:
            app.start_date = config["start_date"]
        if "end_date" in config and config["end_date"] is not None:
            app.end_date = config["end_date"]
        if "start_balance" in config and config["start_balance"] is not None:
            app.start_balance = config["start_balance"]
        if "fees" in config and config["fees"] is not None:
            app.fees = config["fees"]
        if "dry_run" in config and config["dry_run"] is not None:
            app.dry_run = config["dry_run"]
        if "silent" in config and config["silent"] is not None:
            app.silent = config["silent"]
        if "hide_balance" in config and config["hide_balance"] is not None:
            app.hide_balance = config["hide_balance"]
        if "hide_value" in config and config["hide_value"] is not None:
            app.hide_value = config["hide_value"]
        if "hide_net_worth" in config and config["hide_net_worth"] is not None:
            app.hide_net_worth = config["hide_net_worth"]
        if "hide_roi" in config and config["hide_roi"] is not None:
            app.hide_roi = config["hide_roi"]
        if "hide_table" in config and config["hide_table"] is not None:
            app.hide_table = config["hide_table"]
        if "no_header" in config and config["no_header"] is not None:
            app.no_header = config["no_header"]
        if "no_table" in config and config["no_table"] is not None:
            app.no_table = config["no_table"]
        if "debug" in config and config["debug"] is not None:
            app.debug = config["debug"]
        if "test" in config and config["test"] is not None:
            app.test = config["test"]
        if "export" in config and config["export"] is not None:
            app.export = config["export"]
        if "plot" in config and config["plot"] is not None:
            app.plot = config["plot"]
        if "export_filename" in config and config["export_filename"] is not None:
            app.export_filename = config["export_filename"]
        if "plot_filename" in config and config["plot_filename"] is not None:
            app.plot_filename = config["plot_filename"]
        if "timeframe" in config and config["timeframe"] is not None:
            app.timeframe = config["timeframe"]
        if "historical" in config and config["historical"] is not None:
            app.historical = config["historical"]
        if "start_date" in config and config["start_date"] is not None:
            app.start_date = config["start_date"]
        if "end_date" in config and config["end_date"] is not None:
            app.end_date = config["end_date"]
        if "rsi_periods" in config and config["rsi_periods"] is not None:
            app.rsi_periods = config["rsi_periods"]
        if "rsi_upper" in config and config["rsi_upper"] is not None:
            app.rsi_upper = config["rsi_upper"]
        if "rsi_lower" in config and config["rsi_lower"] is not None:
            app.rsi_lower = config["rsi_lower"]
        if "ema1" in config and config["ema1"] is not None:
            app.ema1 = config["ema1"]
        if "ema2" in config and config["ema2"] is not None:
            app.ema2 = config["ema2"]
        if "ema3" in config and config["ema3"] is not None:
            app.ema3 = config["ema3"]
        if "ema4" in config and config["ema4"] is not None:
            app.ema4 = config["ema4"]
        if "ema5" in config and config["ema5"] is not None:
            app.ema5 = config["ema5"]
        if "ema6" in config and config["ema6"] is not None:
            app.ema6 = config["ema6"]
        if "ema7" in config and config["ema7"] is not None:
            app.ema7 = config["ema7"]
        if "ema8" in config and config["ema8"] is not None:
            app.ema8 = config["ema8"]
        if "ema9" in config and config["ema9"] is not None:
            app.ema9 = config["ema9"]
        if "ema10" in config and config["ema10"] is not None:
            app.ema10 = config["ema10"]
        if "ema11" in config and config["ema11"] is not None:
            app.ema11 = config["ema11"]
        if "ema12" in config and config["ema12"] is not None:
            app.ema12 = config["ema12"]
        if "ema13" in config and config["ema13"] is not None:
            app.ema13 = config["ema13"]
        if "ema14" in config and config["ema14"] is not None:
            app.ema14 = config["ema14"]
        if "ema15" in config and config["ema15"] is not None:
            app.ema15 = config["ema15"]
        if "ema16" in config and config["ema16"] is not None:
            app.ema16 = config["ema16"]
        if "ema17" in config and config["ema17"] is not None:
            app.ema17 = config["ema17"]
        if "ema18" in config and config["ema18"] is not None:
            app.ema18 = config["ema18"]
        if "ema19" in config and config["ema19"] is not None:
            app.ema19 = config["ema19"]
        if "ema20" in config and config["ema20"] is not None:
            app.ema20 = config["ema20"]
        if "ema21" in config and config["ema21"] is not None:
            app.ema21 = config["ema21"]
        if "ema22" in config and config["ema22"] is not None:
            app.ema22 = config["ema22"]
        if "ema23" in config and config["ema23"] is not None:
            app.ema23 = config["ema23"]
        if "ema24" in config and config["ema24"] is not None:
            app.ema24 = config["ema24"]
        if "ema25" in config and config["ema25"] is not None:
            app.ema25 = config["ema25"]
        if "ema26" in config and config["ema26"] is not None:
            app.ema26 = config["ema26"]
        if "ema27" in config and config["ema27"] is not None:
            app.ema27 = config["ema27"]
        if "ema28" in config and config["ema28"] is not None:
            app.ema28 = config["ema28"]
        if "ema29" in config and config["ema29"] is not None:
            app.ema29 = config["ema29"]
        if "ema30" in config and config["ema30"] is not None:
            app.ema30 = config["ema30"]
        if "ema31" in config and config["ema31"] is not None:
            app.ema31 = config["ema31"]
        if "ema32" in config and config["ema32"] is not None:
            app.ema32 = config["ema32"]
        if "ema33" in config and config["ema33"] is not None:
            app.ema33 = config["ema33"]
        if "ema34" in config and config["ema34"] is not None:
            app.ema34 = config["ema34"]
        if "ema35" in config and config["ema35"] is not None:
            app.ema35 = config["ema35"]
        if "ema36" in config and config["ema36"] is not None:
            app.ema36 = config["ema36"]
        if "ema37" in config and config["ema37"] is not None:
            app.ema37 = config["ema37"]
        if "ema38" in config and config["ema38"] is not None:
            app.ema38 = config["ema38"]
        if "ema39" in config and config["ema39"] is not None:
            app.ema39 = config["ema39"]
        if "ema40" in config and config["ema40"] is not None:
            app.ema40 = config["ema40"]
        if "ema41" in config and config["ema41"] is not None:
            app.ema41 = config["ema41"]
        if "ema42" in config and config["ema42"] is not None:
            app.ema42 = config["ema42"]
        if "ema43" in config and config["ema43"] is not None:
            app.ema43 = config["ema43"]
        if "ema44" in config and config["ema44"] is not None:
            app.ema44 = config["ema44"]
        if "ema45" in config and config["ema45"] is not None:
            app.ema45 = config["ema45"]
        if "ema46" in config and config["ema46"] is not None:
            app.ema46 = config["ema46"]
        if "ema47" in config and config["ema47"] is not None:
            app.ema47 = config["ema47"]
        if "ema48" in config and config["ema48"] is not None:
            app.ema48 = config["ema48"]
        if "ema49" in config and config["ema49"] is not None:
            app.ema49 = config["ema49"]
        if "ema50" in config and config["ema50"] is not None:
            app.ema50 = config["ema50"]
        if "ema51" in config and config["ema51"] is not None:
            app.ema51 = config["ema51"]
        if "ema52" in config and config["ema52"] is not None:
            app.ema52 = config["ema52"]
        if "ema53" in config and config["ema53"] is not None:
            app.ema53 = config["ema53"]
        if "ema54" in config and config["ema54"] is not None:
            app.ema54 = config["ema54"]
        if "ema55" in config and config["ema55"] is not None:
            app.ema55 = config["ema55"]
        if "ema56" in config and config["ema56"] is not None:
            app.ema56 = config["ema56"]
        if "ema57" in config and config["ema57"] is not None:
            app.ema57 = config["ema57"]
        if "ema58" in config and config["ema58"] is not None:
            app.ema58 = config["ema58"]
        if "ema59" in config and config["ema59"] is not None:
            app.ema59 = config["ema59"]
        if "ema60" in config and config["ema60"] is not None:
            app.ema60 = config["ema60"]
        if "ema61" in config and config["ema61"] is not None:
            app.ema61 = config["ema61"]
        if "ema62" in config and config["ema62"] is not None:
            app.ema62 = config["ema62"]
        if "ema63" in config and config["ema63"] is not None:
            app.ema63 = config["ema63"]
        if "ema64" in config and config["ema64"] is not None:
            app.ema64 = config["ema64"]
        if "ema65" in config and config["ema65"] is not None:
            app.ema65 = config["ema65"]
        if "ema66" in config and config["ema66"] is not None:
            app.ema66 = config["ema66"]
        if "ema67" in config and config["ema67"] is not None:
            app.ema67 = config["ema67"]
        if "ema68" in config and config["ema68"] is not None:
            app.ema68 = config["ema68"]
        if "ema69" in config and config["ema69"] is not None:
            app.ema69 = config["ema69"]
        if "ema70" in config and config["ema70"] is not None:
            app.ema70 = config["ema70"]
        if "ema71" in config and config["ema71"] is not None:
            app.ema71 = config["ema71"]
        if "ema72" in config and config["ema72"] is not None:
            app.ema72 = config["ema72"]
        if "ema73" in config and config["ema73"] is not None:
            app.ema73 = config["ema73"]
        if "ema74" in config and config["ema74"] is not None:
            app.ema74 = config["ema74"]
        if "ema75" in config and config["ema75"] is not None:
            app.ema75 = config["ema75"]
        if "ema76" in config and config["ema76"] is not None:
            app.ema76 = config["ema76"]
        if "ema77" in config and config["ema77"] is not None:
            app.ema77 = config["ema77"]
        if "ema78" in config and config["ema78"] is not None:
            app.ema78 = config["ema78"]
        if "ema79" in config and config["ema79"] is not None:
            app.ema79 = config["ema79"]
        if "ema80" in config and config["ema80"] is not None:
            app.ema80 = config["ema80"]
        if "ema81" in config and config["ema81"] is not None:
            app.ema81 = config["ema81"]
        if "ema82" in config and config["ema82"] is not None:
            app.ema82 = config["ema82"]
        if "ema83" in config and config["ema83"] is not None:
            app.ema83 = config["ema83"]
        if "ema84" in config and config["ema84"] is not None:
            app.ema84 = config["ema84"]
        if "ema85" in config and config["ema85"] is not None:
            app.ema85 = config["ema85"]
        if "ema86" in config and config["ema86"] is not None:
            app.ema86 = config["ema86"]
        if "ema87" in config and config["ema87"] is not None:
            app.ema87 = config["ema87"]
        if "ema88" in config and config["ema88"] is not None:
            app.ema88 = config["ema88"]
        if "ema89" in config and config["ema89"] is not None:
            app.ema89 = config["ema89"]
        if "ema90" in config and config["ema90"] is not None:
            app.ema90 = config["ema90"]
        if "ema91" in config and config["ema91"] is not None:
            app.ema91 = config["ema91"]
        if "ema92" in config and config["ema92"] is not None:
            app.ema92 = config["ema92"]
        if "ema93" in config and config["ema93"] is not None:
            app.ema93 = config["ema93"]
        if "ema94" in config and config["ema94"] is not None:
            app.ema94 = config["ema94"]
        if "ema95" in config and config["ema95"] is not None:
            app.ema95 = config["ema95"]
        if "ema96" in config and config["ema96"] is not None:
            app.ema96 = config["ema96"]
        if "ema97" in config and config["ema97"] is not None:
            app.ema97 = config["ema97"]
        if "ema98" in config and config["ema98"] is not None:
            app.ema98 = config["ema98"]
        if "ema99" in config and config["ema99"] is not None:
            app.ema99 = config["ema99"]
        if "ema100" in config and config["ema100"] is not None:
            app.ema100 = config["ema100"]
        if "ema101" in config and config["ema101"] is not None:
            app.ema101 = config["ema101"]
        if "ema102" in config and config["ema102"] is not None:
            app.ema102 = config["ema102"]
        if "ema103" in config and config["ema103"] is not None:
            app.ema103 = config["ema103"]
        if "ema104" in config and config["ema104"] is not None:
            app.ema104 = config["ema104"]
        if "ema105" in config and config["ema105"] is not None:
            app.ema105 = config["ema105"]
        if "ema106" in config and config["ema106"] is not None:
            app.ema106 = config["ema106"]
        if "ema107" in config and config["ema107"] is not None:
            app.ema107 = config["ema107"]
        if "ema108" in config and config["ema108"] is not None:
            app.ema108 = config["ema108"]
        if "ema109" in config and config["ema109"] is not None:
            app.ema109 = config["ema109"]
        if "ema110" in config and config[""""
    
    if not app:
        raise Exception("No app is passed")

    if isinstance(kucoin_config, dict):
        if "api_key" in kucoin_config or "api_secret" in kucoin_config or "api_passphrase" in kucoin_config:
            print(">>> migrating api keys to kucoin.key <<<", "\n")

            # create 'kucoin.key'
            fh = open("kucoin.key", "w", encoding="utf8")
            fh.write(kucoin_config["api_key"] + "\n" + kucoin_config["api_secret"] + "\n" + kucoin_config["api_passphrase"])
            fh.close()

            if os.path.isfile("config.json") and os.path.isfile("kucoin.key"):
                kucoin_config["api_key_file"] = kucoin_config.pop("api_key")
                kucoin_config["api_key_file"] = "kucoin.key"
                del kucoin_config["api_secret"]
                del kucoin_config["api_passphrase"]

                # read 'Kucoin' element from config.json
                fh = open("config.json", "r", encoding="utf8")
                config_json = ast.literal_eval(fh.read())
                config_json["kucoin"] = kucoin_config
                fh.close()

                # write new 'Kucoin' element
                fh = open("config.json", "w")
                fh.write(json.dumps(config_json, indent=4))
                fh.close()
            else:
                print("migration failed (io error)", "\n")

        app.api_key_file = "kucoin.key"
        if "api_key_file" in args and args["api_key_file"] is not None:
            app.api_key_file = args["api_key_file"]
        elif "api_key_file" in kucoin_config:
            app.api_key_file = kucoin_config["api_key_file"]

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
                    kucoin_config["api_key"] = key
                    kucoin_config["api_secret"] = secret
                    kucoin_config["api_passphrase"] = password
                except Exception:
                    raise RuntimeError(f"Unable to read {app.api_key_file}")

        if "api_key" in kucoin_config and "api_secret" in kucoin_config and "api_passphrase" in kucoin_config and "api_url" in kucoin_config:
            # validates the api key is syntactically correct
            p = re.compile(r"^[A-z0-9]{24,24}$")
            if not p.match(kucoin_config["api_key"]):
                raise TypeError("Kucoin API key is invalid")

            app.api_key = kucoin_config["api_key"]  # noqa: F841

            # validates the api secret is syntactically correct
            p = re.compile(r"^[A-z0-9-]{36,36}$")
            if not p.match(kucoin_config["api_secret"]):
                raise TypeError("Kucoin API secret is invalid")

            app.api_secret = kucoin_config["api_secret"]  # noqa: F841

            # validates the api passphrase is syntactically correct
            p = re.compile(r"^[A-z0-9#$%=@!{},`~&*()<>?.:;_|^/+\[\]]{8,32}$")
            if not p.match(kucoin_config["api_passphrase"]):
                raise TypeError("Kucoin API passphrase is invalid")

            app.api_passphrase = kucoin_config["api_passphrase"]  # noqa: F841

            valid_urls = [
                "https://api.kucoin.com/",
                "https://api.kucoin.com",
                "https://openapi-sandbox.kucoin.com/",
                "https://openapi-sandbox.kucoin.com",
            ]

            # validate Kucoin API
            if kucoin_config["api_url"] not in valid_urls:
                raise ValueError("Kucoin API URL is invalid")

            api_url = kucoin_config["api_url"]  # noqa: F841
            app.base_currency = "BTC"
            app.quote_currency = "GBP"
    else:
        kucoin_config = {}

    config = merge_config_and_args(kucoin_config, args)

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
        app.market = app.base_currency + "-" + app.quote_currency  # noqa: F841

    if "granularity" in config and config["granularity"] is not None:
        if isinstance(config["granularity"], str) and config["granularity"].isnumeric() is True:
            app.granularity = Granularity.convert_to_enum(int(config["granularity"]))
        elif isinstance(config["granularity"], int):
            app.granularity = Granularity.convert_to_enum(config["granularity"])  # noqa: F841
