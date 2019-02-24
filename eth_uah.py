import requests
import time


header = ['pub_date', 'amnt_base', 'amnt_trade', 'id', 'price', 'type', 'user']

csv = open(file='eth_uah.csv', mode='a+', encoding='cp1251')

for key in header:
    csv.write(key + ';')
csv.write('\n')

csv.close()

prev_ids = []
while True:
    csv = open(file='eth_uah.csv', mode='a+', encoding='cp1251')

    resp = requests.get(url='https://btc-trade.com.ua/api/deals/eth_uah')
    resp = resp.json()

    offers_loaded = 0
    for offer in resp:
        if offer['id'] not in prev_ids:
            offers_loaded = offers_loaded + 1
            prev_ids.append(offer['id'])
            for key in header:
                csv.write(str(offer[key]) + ';')
            csv.write('\n')

    csv.close()

    print('eth_uah {} Loaded {} new offers'.format(time.ctime(), offers_loaded))

    time.sleep(61*61)
