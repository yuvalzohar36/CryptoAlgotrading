from requests import Request, Session
import json


class CoinMarketCap:

    @staticmethod
    def get_data(symbol, local_config):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {'symbol': symbol}
        headers = {'Accept': 'application/json', 'X-CMC_PRO_API_KEY': local_config["CoinMarketCap"]["coinmarketcap_token"]}
        session = Session()
        session.headers.update(headers)
        resp = session.get(url, params=parameters)
        price = json.loads(resp.text)
        return price

