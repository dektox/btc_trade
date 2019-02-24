#!/usr/bin/python
# -*- coding: cp1251 -*-


import requests
import time
from csv import reader


class Parser:
    def __init__(self, pair):
        self.pair = pair
        self.header = ['pub_date', 'amnt_base', 'amnt_trade', 'id', 'price', 'type', 'user']

        self.prev_ids = []
        with open('{}.csv'.format(self.pair), 'r', encoding='cp1251') as file:
            order_ids = reader(file, delimiter=';')
            for order_id in order_ids:
                if order_id[3] != 'id':
                    self.prev_ids.append(int(order_id[3]))

    def run(self):
        try:
            resp = requests.get(url='https://btc-trade.com.ua/api/deals/{}'.format(self.pair))
            resp = resp.json()
            offers_loaded = 0

            csv = open(file='{}.csv'.format(self.pair), mode='a+', encoding='cp1251')

            for offer in resp:
                if offer['id'] not in self.prev_ids:
                    offers_loaded = offers_loaded + 1
                    self.prev_ids.append(offer['id'])
                    for key in self.header:
                        csv.write(str(offer[key]) + ';')
                    csv.write('\n')

            csv.close()

            print('{} {} Loaded {} new offers'.format(self.pair, time.ctime(), offers_loaded))
        # except KeyboardInterrupt:
        #     return
        except Exception as ex:
            with open('errors_{}.log'.format(self.pair), 'a+', encoding='cp1251') as log_file:
                log_file.write(str(ex) + '\n')
                print('ERROR IN {} !!!'.format(self.pair))
            time.sleep(301)
        else:
            time.sleep(5)


def main():
    parsers = []
    for pair in ['bch_uah', 'btc_uah', 'dash_btc', 'dash_uah', 'doge_btc', 'doge_uah', 'eth_uah', 'iti_uah', 'krb_uah',
                 'ltc_btc', 'ltc_uah', 'nvc_btc', 'nvc_uah', 'ppc_btc', 'sib_uah', 'xmr_uah', 'zec_uah']:
        parser = Parser(pair=pair)
        parsers.append(parser)

    while True:
        for parser in parsers:
            parser.run()
        time.sleep(61*61)


if __name__ == '__main__':
    main()
