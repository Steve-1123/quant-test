import datetime
import hmac
import base64
from .constant import *

def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = url + str(key) + '=' + str(value) + '&'
    print('url:',url)
    return url[0:-1]

def get_timestamp():
    now = datetime.datetime.utcnow()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"

def get_header(api_key, sign, timestamp, passphrase, flag):
    header = dict()
    header[CONTENT_TYPE] = APPLICATION_JSON
    header[OK_ACCESS_KEY] = api_key
    header[OK_ACCESS_SIGN] = sign
    header[OK_ACCESS_TIMESTAMP] = str(timestamp)
    header[OK_ACCESS_PASSPHRASE] = passphrase
    header['x-simulated-trading'] = flag
    print('header: ',header)
    return header

def signature(message, secretKey):
    mac = hmac.new(bytes(secretKey, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)

def pre_hash(timestamp, method, request_path, body):
    print('body: ',body)
    return str(timestamp) + str.upper(method) + request_path + body
