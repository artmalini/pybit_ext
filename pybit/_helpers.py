import time
import re
import copy
import requests


def generate_timestamp():
    attempt = 0
    timedata = 0
    while True and attempt < 12 :
        try:
            timedata = requests.get('https://api-testnet.bybit.com/v3/public/time')
            break
        except:
            attempt += 1
            time.sleep(1)
    timestamp_offset = int(timedata.json()['result']['timeSecond']) - int(time.time() * 1000)
    offset = int(time.time() * 1000 + timestamp_offset)
    #add user-agent
    #add auth info
    expires = str(offset)+"000"
    return expires
    """
    Return a millisecond integer timestamp.
    """
    #return int(time.time() * 10 ** 3)


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


def make_public_kwargs(private_kwargs):
    public_kwargs = copy.deepcopy(private_kwargs)
    public_kwargs.pop("api_key", "")
    public_kwargs.pop("api_secret", "")
    return public_kwargs
