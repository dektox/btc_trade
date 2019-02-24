import requests
import time
import selenium
from selenium import webdriver
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('btc-trade-ua-ec5e37f113cf.json', scope)

client = gspread.authorize(creds)
REPORT_NAME='btc_uah'
REPORT_SHEET_NAME = 'btc_uah'
START_RAW=1
END_RAW=200000

header = ['pub_date', 'amnt_base', 'amnt_trade', 'id', 'price', 'type', 'user']

prev_ids = []
while True:
    try:
        resp = requests.get(url='https://btc-trade.com.ua/api/deals/btc_uah')
        resp = resp.json()
        sheet = client.open(REPORT_NAME).worksheet(REPORT_SHEET_NAME)
        offers_loaded = 0
        for offer in resp:
            if offer['id'] not in prev_ids:
                offers_loaded = offers_loaded + 1
                prev_ids.append(offer['id'])
                for key in header:
                    sheet.update_cell(str(START_RAW + offers_loaded),key, str(str(offer[key])))

        print('btc_uah  {} Loaded {} new offers'.format(time.ctime(), offers_loaded))

        time.sleep(1)
    except Exception as ex:
        with open('errors_{}.log'.format(pair), 'a+', encoding='utf8') as log_file:
            log_file.write(str(ex)+'\n')
        time.sleep(5)
    else:
        time.sleep(61*61)