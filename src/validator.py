from datetime import datetime


def to_date(string):
    """ :raises ValueError """
    return datetime.strptime(string, '%Y-%m-%d').date()


def to_price_type(string):
    """ :raises ValueError """
    string = string.lower()
    if string not in ('open', 'high', 'low', 'close'):
        raise ValueError
    return string
