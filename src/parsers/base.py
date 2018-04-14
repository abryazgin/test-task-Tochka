import requests
from lxml import html
from datetime import datetime


class BasePageParser:
    """ Базовый класс для парсинга страниц """
    def __init__(self, url):
        self.url = url
        self.html = None
        self.download()

    def download(self):
        """ Скачиваем содержимое страницы """
        print('DOWNLOADING: {}'.format(self.url))
        self.html = html.fromstring(requests.get(self.url).text)

    def _to_date(self, string, frmt='%m/%d/%Y'):
        """ Приведение строки к дате """
        return datetime.strptime(string, frmt).date() if string else None

    def _to_float(self, string):
        """ Приведение строки к числу """
        return float(string.replace(',', '')) if string else None


class BaseTablePageParser(BasePageParser):
    """ Базовый класс для парсинга таблиц со страниц"""
    def _get_table(self):
        raise NotImplementedError

    def _prepare_row(self, row_obj):
        raise NotImplementedError

    def __iter__(self):
        """ Итерируемся по чистым данным """
        table_obj = self._get_table()
        for row_obj in table_obj:
            row = self._prepare_row(row_obj)
            # чистим от строк, в которых нет значений - они нам не интересны
            # TODO сделать настройкой?
            if any(row):
                yield row
