from database import models as md


def save(session, company_code, date, high, low, open_, close, volume):
    obj = md.StockPrice(
        company_code=company_code, date=date, high=high,
        low=low, open=open_, close=close, volume=volume)
    session.add(obj)
    session.flush()
    return obj


def get(session, company_code, date):
    return session.query(md.StockPrice).filter_by(
        company_code=company_code, date=date).first()


def get_or_save(session, company_code, date, high, low, open_, close, volume):
    obj = get(session=session, company_code=company_code, date=date)
    if obj:
        return obj
    return save(
        session=session, company_code=company_code, date=date,
        high=high, low=low, open_=open_, close=close, volume=volume)
