import config
from collections import namedtuple

from .base import BaseTablePageParser


def parse_prices(symbol):
    url = config.SITE_PRICES_URL.format(symbol=symbol.lower())
    return PricePageParser(url)


""" Контейнер для результатов парсинга таблицы с Ценами """
RowPricePage = namedtuple('RowPricePage', (
    'date', 'open', 'high', 'low', 'close', 'volume'))


class PricePageParser(BaseTablePageParser):
    def _get_table(self):
        """ Ищем таблицу с данными (работаем с tbody) """
        return self.html.xpath(
            './/div[@id = "historicalContainer"]/div/table/tbody')[0]

    def _prepare_row(self, row_obj):
        """ Подготавливаем строку чистых данных (работаем с tr)"""
        date, open, high, low, close, volume = [
            el.text.strip() if el.text is not None else None for el in row_obj]
        row = RowPricePage(
            date=self._to_date(date),
            open=self._to_float(open),
            high=self._to_float(high),
            low=self._to_float(low),
            close=self._to_float(close),
            volume=self._to_float(volume),
        )
        return row
