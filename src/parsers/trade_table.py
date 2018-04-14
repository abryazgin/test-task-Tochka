import config
from collections import namedtuple

from .base import BaseTablePageParser


def parse_trade(symbol, page=1):
    url = config.SITE_TRADES_URL.format(symbol=symbol.lower(), n=page)
    return TradePageParser(url)


""" Контейнер для результатов парсинга таблицы с Торговыми операциями """
RowTradePage = namedtuple('RowTradePage', (
    'insider', 'relation', 'last_date', 'transaction_type', 'ownertype',
    'shares_traded', 'last_price', 'shares_held'))


class TradePageParser(BaseTablePageParser):

    def get_max_page_number(self):
        """ Ищем количество страниц по акциям (работаем с pager) """
        pages = self.html.xpath(
            './/ul[@id = "pager"]/ul[@class = "pager"]/li/a')
        max_page_number = 1
        for page_obj in pages:
            if page_obj.text.isdigit():
                cur_number = int(page_obj.text)
                if cur_number > max_page_number:
                    max_page_number = cur_number
        return max_page_number

    def _get_table(self):
        """ Ищем таблицу с данными (работаем с tbody) """
        return self.html.xpath(
            './/div[@class = "genTable"]/table')[0][1:]

    def _prepare_row(self, row_obj):
        """ Подготавливаем строку чистых данных (работаем с tr)"""
        # insider находится в <a>, поэтому его берем по особому
        # insider - это первый лемент и н лежит глубже (поэтому [0][0])
        insider = row_obj[0][0].text.strip()
        (
            relation, last_date, transaction_type, ownertype,
            shares_traded, last_price, shares_held
        ) = [
            el.text.strip() if el.text is not None else None for el in row_obj[1:]]
        row = RowTradePage(
            insider=insider,
            relation=relation,
            last_date=self._to_date(last_date),
            transaction_type=transaction_type,
            ownertype=ownertype,
            shares_traded=self._to_float(shares_traded),
            last_price=self._to_float(last_price),
            shares_held=self._to_float(shares_held)
        )
        return row
