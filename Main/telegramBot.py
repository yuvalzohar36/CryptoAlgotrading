import requests
import time
from datetime import datetime


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


def main_tg_bot(wallet, token, delay):
    badi_bot = BotHandler(token)
    chat_id = -1001611250626  # current_update['message']['chat']['id']
    new_offset = 0
    print('Telegram Bot Active\n')
    time.sleep(180)
    while True:
        # all_updates = badi_bot.get_updates(new_offset)
        # if len(all_updates) > 0:
        #     for current_update in all_updates:
        #         first_update_id = current_update['update_id']
        #         if 'text' in current_update['message']:
        #             if '/balance' in current_update['message']['text'] :

                        #prices = wallet.get_all_prices()
                        info = wallet.relevant_account_info()
                        total = 0
                        lst1 = []
                        lst4 = []
                        for i in info['asset']:
                            lst1.append(i)
                            lst4.append(wallet.currency_price(i))

                        lst2 = []
                        for i in info['free']:
                            lst2.append(i)
                        lst3 = []
                        for i in info['locked']:
                            lst3.append(i)

                        str1 =''
                        now = datetime.now()

                        print("now =", now)

                        # dd/mm/YY H:M:S
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                        str1 +=str(dt_string)
                        str1 += "\n\n"
                        for i in range(len(lst1)):
                            str1 += "Symbol: "+ str(lst1[i]) + "\n" + f"Amount: {str(lst2[i])}\nValue: {lst4[i]*lst2[i]}$\nLocked: {lst3[i]}\n\n"
                            total += lst4[i]*lst2[i]
                        str1 += f"\nTotal: {total}$"
                        badi_bot.send_message(chat_id,str1)
                        time.sleep(delay)



                        # for i in range(len(info)):
                        #     for j in range(len(prices)):
                        #         if prices[j]['symbol'] == info['asset'][i] + "USDT":
                        #             priced = prices[j]['price']
                        #
                        #         elif info['asset'][i] == "USDT":
                        #             priced = 1
                        #     str1 += "★ " + info['asset'][i] + "\n📊𝐑𝐚𝐭𝐞 " + str(priced) + "\n💰𝐅𝐫𝐞𝐞 " + \
                        #             str(info['free'][i]) + "\n💲𝐓𝐨𝐭𝐚𝐥 " + str(
                        #         int(float(priced)) * int(float(info['free'][i]))) + "$ \n\n"
                        #     total += int(float(priced) * float(info['free'][i]))
                        # str1 += "__________________________\n\n💵 Total Balance: " + str(total) + "$"

              #  new_offset = first_update_id + 1
