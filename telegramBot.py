import requests
import time


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset, 'allowed_updates': ["message", 'callback_query']}
        resp = requests.get(self.api_url + method, params)
        count = 0
        while 'result' not in resp.json():
            time.sleep(1)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp


def main_tg_bot(wallet, token):
    badi_bot = BotHandler(token)
    new_offset = 0
    print('Telegram Bot Active\n')
    while True:
        all_updates = badi_bot.get_updates(new_offset)
        if len(all_updates) > 0:
            for current_update in all_updates:
                first_update_id = current_update['update_id']
                if 'text' in current_update['message']:
                    if '/balance' in current_update['message']['text']:
                        prices = wallet.get_all_prices()
                        chat_id = current_update['message']['chat']['id']
                        info = wallet.relevant_account_info()
                        str1 = ""
                        total = 0
                        for i in range(len(info)):
                            for j in range(len(prices)):
                                if prices[j]['symbol'] == info[i]['asset'] + "USDT":
                                    priced = prices[j]['price']

                                elif info[i]['asset'] == "USDT":
                                    priced = 1
                            str1 += "★ " + info[i]['asset'] + "\n📊𝐑𝐚𝐭𝐞 " + str(priced) + "\n💰𝐅𝐫𝐞𝐞 " + info[i][
                                'free'] + "\n💲𝐓𝐨𝐭𝐚𝐥 " + str(
                                int(float(priced)) * int(float(info[i]['free']))) + "$ \n\n"
                            total += int(float(priced) * float(info[i]['free']))
                        str1 += "__________________________\n\n💵 Total Balance: " + str(total) + "$"
                        badi_bot.send_message(chat_id, str1)
                new_offset = first_update_id + 1
