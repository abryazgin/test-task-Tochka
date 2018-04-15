from database import models as md
from datetime import datetime, timedelta
from collections import namedtuple


def list_last(company_code, from_date=None, to_date=None):
    """
    Получение последних цен на акции.
    По умолчанию - за последний 91 день ~ 3 месяца (включая сегодня)
    """
    company = md.Company.query.get_or_404(company_code)

    from_date = from_date or datetime.now().date() - timedelta(days=90)
    q = md.StockPrice.query.filter(
        md.StockPrice.company_code == company_code).filter(
        md.StockPrice.date >= from_date)
    if to_date:
        q = q.filter(md.StockPrice.date < to_date)
    q = q.order_by(md.StockPrice.date.desc())
    return company, iter(q)


DeltaStockPrice = namedtuple('DeltaStockPrice', (
    'company_code', 'date', 'high', 'low', 'open', 'close', 'volume',
))


def list_deltas(company_code, from_date=None, to_date=None):
    """
    Получение изменений цен
    """
    from_date = from_date or datetime.now().date() - timedelta(days=90)

    company, prices = list_last(
        company_code=company_code,
        from_date=from_date - timedelta(days=1),
        to_date=to_date)

    def gen():
        cur_price = next(prices)
        for prev_price in prices:
            yield DeltaStockPrice(
                company_code=cur_price.company_code,
                date=cur_price.date,
                high=cur_price.high - prev_price.high,
                low=cur_price.low - prev_price.low,
                open=cur_price.open - prev_price.open,
                close=cur_price.close - prev_price.close,
                volume=cur_price.volume,
            )
            cur_price = prev_price
    return company, gen()


DeltaInterval = namedtuple('DeltaInterval', (
    'from_date', 'to_date', 'length', 'delta',
))


def get_minimal_delta_intervals(company_code, delta, price_type, limit=20):
    """
        Получение минимальных интервалов с изменением цены <price_type>
    на акции <company_code> не меньше чем на <delta>

    Принцип:
    0) ставим "дата с" = "дата по" = началу
    1) сдвигаем "дата с" вниз пока не превысим дельту
    2) как только превысили дельту сохраняем интервал как кандидата в памяти
    3) сдвигаем "дату по" вниз, если при сдвиге дельта не меньше порога,
        То сохраняем интервал как нового кадидата и повторяем п.3.
        Иначе - сохраняем текущего кандидата и переходим к п.1

    по исчерпании дат, возвращаем первые <limit> интервалов сортируя
    их по величине интервала от меньшего к большему

    :param company_code: код акции/компаниии
    :param delta: значение порога изменения
    :param price_type: тип цены (open/high/low/close)
    :param limit: количество интервалов
    """
    intervals = []
    # делаем копию итератора дельт
    from itertools import tee
    company, deltas = list_deltas(company_code=company_code)
    deltas_from, deltas_to = tee(deltas, 2)

    def add_interval(from_delta, to_delta, delta_):
        intervals.append(
            DeltaInterval(
                from_date=from_delta.date,
                to_date=to_delta.date,
                length=(to_delta.date - from_delta.date).days + 1,
                delta=delta_,
            )
        )

    cur_delta = 0
    candidate = None

    for to in deltas_to:
        if candidate:
            if abs(cur_delta) >= delta:
                # old from, new to
                candidate = candidate[0], to, cur_delta
                # уменьшаем дельту на "убранный" день
                cur_delta -= getattr(to, price_type)
                continue
            else:
                add_interval(*candidate)
                candidate = None
        for from_ in deltas_from:
            # увеличиваем дельту на "добавленный" день
            cur_delta += getattr(from_, price_type)
            if abs(cur_delta) >= delta:
                candidate = from_, to, cur_delta
                break
        # уменьшаем дельту на "убранный" день
        cur_delta -= getattr(to, price_type)
    return company, sorted(
        intervals, key=lambda v: (v.length, -abs(v.delta)))[:limit]


def get_or_save(session, company_code, date, high, low, open_, close, volume):
    """ Дай если есть. Если нет - создай и верни """
    obj = session.query(md.StockPrice).filter_by(
        company_code=company_code, date=date).first()
    if not obj:
        obj = md.StockPrice(
            company_code=company_code, date=date, high=high,
            low=low, open=open_, close=close, volume=volume)
        session.add(obj)
        session.flush()
    return session.query(md.StockPrice).filter_by(
        company_code=company_code, date=date).first()


def marshall(obj):
    """ Маршализация """
    d = dict()
    d['date'] = obj.date
    d['high'] = obj.high
    d['low'] = obj.low
    d['open'] = obj.open
    d['close'] = obj.close
    d['volume'] = obj.volume
    return d
