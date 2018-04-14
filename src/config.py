import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgres://localhost/test_tochka?user=postgres&password=1'

SITE_PRICES_URL = 'https://www.nasdaq.com/symbol/{symbol}/historical'
SITE_TRADES_URL = 'https://www.nasdaq.com/symbol/{symbol}/insider-trades'
