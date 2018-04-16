from database import models as md
from datetime import datetime, timedelta
from collections import namedtuple

db = md.db


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
    company = md.Company.query.get_or_404(company_code)

    assert price_type in ('open', 'high', 'low', 'close')

    # TODO add temporary tables and indexes on them (for example: `deltas`)
    query = db.session.execute('''
        WITH RECURSIVE deltas (D, DELTA) AS (
            SELECT
                    CUR.DATE, CUR.{price_type} - PREV.{price_type}
                FROM
                    stock_price CUR
                    JOIN stock_price PREV
                        ON CUR.DATE = PREV.DATE + INTERVAL '1 DAY'
                        AND CUR.COMPANY_CODE = PREV.COMPANY_CODE
                WHERE
                    CUR.COMPANY_CODE = :company_code
        ), intervals (I_FROM, I_TO, LENGTH, DELTA) AS (
            SELECT
                    BASE.D AS I_FROM, BASE.D AS I_TO, 1 AS LENGTH, BASE.DELTA
                FROM
                    deltas BASE
            UNION ALL
            SELECT
                    I.I_FROM AS I_FROM, D.D AS I_TO,
                    I.LENGTH + 1 AS LENGTH, I.DELTA + D.DELTA AS DELTA
                FROM
                    intervals I
                    JOIN deltas D
                        ON I.I_TO + INTERVAL '1 DAY' = D.D
                        AND SIGN(I.DELTA + D.DELTA) = SIGN(I.DELTA)
                        AND ABS(I.DELTA) < :delta
        )
        SELECT
                I.I_FROM, I.I_TO, I.LENGTH, I.DELTA
            FROM
                intervals I
                LEFT JOIN intervals I_INNER
                    ON I.I_FROM < I_INNER.I_FROM
                    AND I.I_TO >= I_INNER.I_TO
                    AND ABS(I_INNER.DELTA) >= :delta
            WHERE
                ABS(I.DELTA) >= :delta
                AND I_INNER.I_FROM IS NULL
            ORDER BY
                I.LENGTH, ABS(I.DELTA) DESC
            LIMIT :limit;
        '''.format(price_type=price_type), dict(
            limit=limit, delta=delta, company_code=company.code))
    return company, (
        DeltaInterval(row[0], row[1], row[2], row[3]) for row in query
    )


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
