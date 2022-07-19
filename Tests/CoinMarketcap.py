from requests import Request, Session
import json


class CoinMarketcap:

    @staticmethod
    def get_price():
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {'slug': 'bitcoin', 'convert': 'USDT'}
        headers = {'Accept': 'application/json', 'X-CMC_PRO_API_KEY': '0dd29fab-3298-43f8-b291-3ee1eaf76982'}

        session = Session()
        session.headers.update(headers)

        resp = session.get(url, params=parameters)
        price = json.loads(resp.text)['data']['1']['quote']#['price']
        print(price)
        return True


CoinMarketcap.get_price()

