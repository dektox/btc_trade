import threading
import requests
import time
from csv import reader


class Parser(threading.Thread):
    def __init__(self, pair):
        super(Parser, self).__init__()
        self.daemon = True
        self.pair = pair

    def run(self):
        header = ['pub_date', 'amnt_base', 'amnt_trade', 'id', 'price', 'type', 'user']
        prev_ids = []
        with open('{}.csv'.format(self.pair), 'r') as file:
            order_ids = reader(file, delimiter=';')
            for order_id in order_ids:
                if order_id[3] != 'id':
                    prev_ids.append(int(order_id[3]))

        while True:
            try:
                resp = requests.get(url='https://btc-trade.com.ua/api/deals/{}'.format(self.pair))
                resp = resp.json()
                offers_loaded = 0
                csv = open(file='{}.csv'.format(self.pair), mode='a+', encoding='cp1251')

                for offer in resp:
                    if offer['id'] not in prev_ids:
                        offers_loaded = offers_loaded + 1
                        prev_ids.append(offer['id'])
                        for key in header:
                            csv.write(str(offer[key]) + ';')
                        csv.write('\n')

                csv.close()

                print('{} {} Loaded {} new offers'.format(self.pair, time.ctime(), offers_loaded))
            except KeyboardInterrupt:
                break
            except Exception as ex:
                with open('errors_{}.log'.format(self.pair), 'a+', encoding='utf8') as log_file:
                    log_file.write(str(ex) + '\n')
                time.sleep(5)
            else:
                time.sleep(2)


def main():
    p1 = Parser('btc_uah')
    p2 = Parser('krb_uah')

    p1.start()
    p2.start()

    p1.join()
    p2.join()


if __name__ == '__main__':
    main()

