'''
Goal: extract relevant fields from Robinhood trade data to make CSV for 1099b form for Uncle Sam

Required fields:
Description (100 shares of NTDOY)
Date Sold (3/14/2020)
Sales Proceeds ($543.21)
Date Acquired (VARIOUS or 1/23/2020)
Cost ($654.32)
Wash Sale (W)
Adjustment Amount ($0.32)
ST/LT (LT or ST, ST = less than 1 year between buy and sell date)
Reporting Category (A-D)

Author: Vincent Stevenson
'''

import json
import csv

class MakeCleanTradeDataCSV:
    def __init__(self):
        self.gen_csv()

    def gen_csv(self):
        summarized_trade_data = []
        with open('trade_data.json') as f:
            trade_data = json.load(f)

            for k,v in trade_data.items():
                state = v['state'] # filled or cancelled - only care about filled orders
                if state == 'filled':
                    ticker = v['symbol']
                    qty = v['cumulative_quantity']
                    price = v['average_price']
                    try: price_currency = v['total_notional']['currency_code']
                    except: price_currency = None
                    settlement_date = v['settlement_date']
                    action = v['side']
                    data = {
                        "ticker": ticker,
                        "qty": qty,
                        "price": price,
                        "price_currency": price_currency,
                        "date_of_transation": settlement_date,
                        "action": action
                    }
                    summarized_trade_data.append(data)

        csv_cols = summarized_trade_data[0].keys()
        csv_path = 'clean_trade_data.csv'
        with open(csv_path, 'w', newline='') as f:
            w = csv.DictWriter(f,fieldnames=csv_cols)
            w.writeheader()
            for d in summarized_trade_data:
                w.writerow(d)

        print('Created a CSV containing summarized trade data at: .\{}'.format(csv_path))
