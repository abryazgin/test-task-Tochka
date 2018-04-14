#!/usr/bin/env python
import os
import sys

import click

rootdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

sys.path.append(os.path.join(rootdir, 'src'))

from main import db
from parsers import parse_prices, parse_trade
import controllers as ctl


@click.command()
@click.argument(
    'filename',
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    )
)
def parse_using_file(filename):
    with open(filename) as f:
        for symbol in f:
            symbol = symbol.strip().upper()
            parse_and_save_symbol_info(symbol=symbol)


def parse_and_save_symbol_info(symbol):
    print('work with `{}`'.format(symbol))
    ctl.company.get_or_save(session=db.session, code=symbol)
    print('* save prices')
    for price_row in parse_prices(symbol=symbol):
        ctl.stockprice.get_or_save(
            session=db.session,
            company_code=symbol,
            date=price_row.date,
            high=price_row.high,
            low=price_row.low,
            open_=price_row.open,
            close=price_row.close,
            volume=price_row.volume)
        db.session.commit()
    print('* save trades')
    for trade_row in parse_trade(symbol=symbol):
        ctl.relationtype.get_or_save(
            session=db.session, code=trade_row.relation)
        ctl.ownertype.get_or_save(
            session=db.session, code=trade_row.ownertype)
        insider = ctl.insider.get_or_save(
            session=db.session, name=trade_row.insider, company_code=symbol,
            relationtype_code=trade_row.relation,
            ownertype_code=trade_row.ownertype)
        ctl.transactiontype.get_or_save(
            session=db.session, code=trade_row.transaction_type)
        ctl.stockinsidertrade.get_or_save(
            session=db.session,
            last_date=trade_row.last_date,
            shares_traded=trade_row.shares_traded,
            last_price=trade_row.last_price,
            shares_held=trade_row.shares_held,
            insider_id=insider.id,
            transactiontype_code=trade_row.transaction_type)
        db.session.commit()


if __name__ == '__main__':
    parse_using_file()
