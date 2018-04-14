#!/usr/bin/env python
import os
import sys

import click

rootdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

sys.path.append(os.path.join(rootdir, 'src'))


import config
from main import db
from parsers import parse_prices, parse_trade
from task_manager import TaskManager
import controllers as ctl


@click.command()
@click.argument(
    'filepath',
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    )
)
@click.argument('n', type=click.INT, default=1)
def parse_using_file(filepath, n):
    """
    Собственно загрузка данных

     Создаем менеджер задач, читаем из файла код акции и тут же кладем задания
     на скачивание данныъ по этой акции

     В конце ждем выполнения всех задач и выходим

    :param filepath: путь до файла
    :param n: количество потоков для скачивания
    :return:
    """
    tm = TaskManager(n)
    with open(filepath) as f:
        for symbol in f:
            symbol = symbol.strip().upper()
            create_tasks(symbol=symbol, tm=tm)

    tm.finish()


def create_tasks(symbol, tm):
    """ Формируем задания на скачивание данных по конкретной акции """
    ctl.company.get_or_save(session=db.session, code=symbol)
    tm.add(task_save_prices, (symbol, ))
    tm.add(task_save_trades_with_subpages, (symbol, tm, ))


def task_save_prices(symbol):
    """ Сохранение цен на акции """
    parser = parse_prices(symbol=symbol)
    for price_row in parser:
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


def task_save_trades_with_subpages(symbol, tm):
    """
    Скачиваем первую страницу операций, смотрим сколько всего страниц указано
    И ставим необходимые на скачивание
    """
    parser = parse_trade(symbol=symbol, page=1)
    page_limit = min(
        parser.get_max_page_number(), config.SITE_TRADES_PAGE_LIMIT)
    for new_page_number in range(2, page_limit + 1):
        # стивим задачи на скачивание следующих страниц
        tm.add(task_save_trades, (symbol, new_page_number))
    save_trades(parser, symbol, 1)


def task_save_trades(symbol, page_number):
    """
    Скачиваем произвольную страницу операций
    """
    parser = parse_trade(symbol=symbol, page=page_number)
    save_trades(parser, symbol, page_number)


def save_trades(parser, symbol, page_number):
    """ Сохранение страницы операций в БД """
    for trade_row in parser:
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
