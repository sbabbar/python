'''Monitors portfolio value given past purchase history.

TODOs:
   XXX Look inside stocks.txt for ticker symbols (parse the file).
   XXX Get the current price for a ticker symbol (REST service in the cloud).
   XXX Calculate the net gain/loss both overall and per symbol.
'''

import csv
import urllib
import sys


def read_portfolio(filename='notes/stocks.txt'):
    "Reads portfolio holdings info from a purchase history file."
    holdings = []

    with open(filename) as fh:
        stock_reader = csv.reader(fh)
        for line in stock_reader:
            ticker, shares, price = line
            holdings.append((ticker, int(shares), float(price)))

    return holdings

url_template = "http://finance.yahoo.com/d/quotes.csv?s=%s&f=l1"


def get_current_stock_price(ticker):
    "Obtains the current price from Yahoo Finance's RESTful API."

    url = url_template % ticker

    u = urllib.urlopen(url)
    data = u.read()
    u.close()

    return float(data)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'notes/stocks.txt'

    total = 0.0
    returns = {}
    for ticker, shares, purchase_price in read_portfolio(filename):
        current_price = get_current_stock_price(ticker)
        net_gain_loss = (current_price - purchase_price) * shares
        total += net_gain_loss


        # A dict-specific approach
        returns[ticker] = returns.setdefault(ticker, 0.0) + net_gain_loss

    for ticker, contrib in returns.iteritems():
        print "%5s %10.2f" % (ticker, contrib)
    print "=" * 20
    print "TOTAL %10.2f" % total

