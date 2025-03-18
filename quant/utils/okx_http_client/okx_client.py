from conf import OKXConfig
from .constant import *
from .utils import *
import json, requests

class OKXHttpClient:
    def __init__(self):
        self.FLAG = OKXConfig.FLAG
        self.API_KEY = OKXConfig.API_KEY
        self.SECRET_KEY = OKXConfig.SECRET_KEY
        self.PASSPHRASE = OKXConfig.PASSPHRASE
        self.CLIENT_URL = CLIENT_URL

    def _request(self, method, request_path, params):
        if method == GET:
            request_path = request_path + parse_params_to_str(params=params)
        timestamp = get_timestamp()
        body = json.dumps(params) if method == POST else ""
        pre_str = pre_hash(timestamp, method, request_path, str(body))
        sign = signature(pre_str, self.SECRET_KEY)
        header = get_header(api_key=self.API_KEY, sign=sign, timestamp=timestamp, passphrase=self.PASSPHRASE, flag=self.FLAG)
        print(self.CLIENT_URL+request_path)
        resp = requests.get(url=self.CLIENT_URL+request_path, params=params, headers=header, data=body)

        if resp.status_code != 200:
            print('request failed, msg: ', resp.json())
        return resp.json()
    
    def get_account(self, ccy=''):
        params = {}
        if ccy:
            params['ccy'] = ccy
        return self._request(GET, ACCOUNT_INFO, params)
