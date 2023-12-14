import time
import re
import copy
import requests


def generate_timestamp():
    attempt = 0
    timedata = 0
    while True and attempt < 12 :
        try:
            timedata = requests.get('https://api-testnet.bybit.com/v5/market/time')
            break
        except:
            attempt += 1
            time.sleep(1)

    timestamp_offset = 0
    try:
        timestamp_offset = int(timedata.json()['result']['timeSecond']) - int(time.time() * 1000)
    except Exception as e:
        return int(time.time() * 10**3)
    
    offset = int(time.time() * 1000 + timestamp_offset)
    expires = str(offset)+"000"
    return int(expires)


def identify_ws_method(input_wss_url, wss_dictionary):
    """
    This method matches the input_wss_url with a particular WSS method. This
    helps ensure that, when subscribing to a custom topic, the topic
    subscription message is sent down the correct WSS connection.
    """
    path = re.compile("(wss://)?([^/\s]+)(.*)")
    input_wss_url_path = path.match(input_wss_url).group(3)
    for wss_url, function_call in wss_dictionary.items():
        wss_url_path = path.match(wss_url).group(3)
        if input_wss_url_path == wss_url_path:
            return function_call


def find_index(source, target, key):
    """
    Find the index in source list of the targeted ID.
    """
    return next(i for i, j in enumerate(source) if j[key] == target[key])


def make_private_args(args):
    """
    Exists to pass on the user's arguments to a lower-level class without
    giving the user access to that classes attributes (ie, passing on args
    without inheriting the parent class).
    """
    args.pop("self")
    return args


def make_public_kwargs(private_kwargs):
    public_kwargs = copy.deepcopy(private_kwargs)
    public_kwargs.pop("api_key", "")
    public_kwargs.pop("api_secret", "")
    return public_kwargs


def are_connections_connected(active_connections):
    for connection in active_connections:
        if not connection.is_connected():
            return False
    return True


def is_inverse_contract(symbol: str):
    if re.search(r"(USD)([HMUZ]\d\d|$)", symbol):
        return True


def is_usdt_perpetual(symbol: str):
    if symbol.endswith("USDT"):
        return True


def is_usdc_perpetual(symbol: str):
    if symbol.endswith("USDC"):
        return True


def is_usdc_option(symbol: str):
    if re.search(r"[A-Z]{3}-.*-[PC]$", symbol):
        return True
