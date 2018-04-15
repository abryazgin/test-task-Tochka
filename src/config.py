import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgres://localhost/test_tochka?user=postgres&password=1'

SITE_PRICES_URL = 'https://www.nasdaq.com/symbol/{symbol}/historical'
SITE_TRADES_URL = 'https://www.nasdaq.com/symbol/{symbol}/insider-trades?page={n}'
SITE_TRADES_PAGE_LIMIT = 10
STATIC_FOLDER = 'static'

# избавляемся от мусорных ворнингов
# https://github.com/mitsuhiko/flask-sqlalchemy/issues/365
SQLALCHEMY_TRACK_MODIFICATIONS = False
