from database import models as md


def save(
        session, last_date, shares_traded, last_price,
        shares_held, insider_id, transactiontype_code):
    obj = md.StockInsiderTrade(
        last_date=last_date,
        shares_traded=shares_traded,
        last_price=last_price,
        shares_held=shares_held,
        insider_id=insider_id,
        transactiontype_code=transactiontype_code,
    )
    session.add(obj)
    session.flush()
    return obj


def find(session, insider_id, transactiontype_code, last_date):
    return session.query(md.StockInsiderTrade).filter_by(
        insider_id=insider_id, transactiontype_code=transactiontype_code,
        last_date=last_date).first()


def get_or_save(
        session, last_date, shares_traded, last_price,
        shares_held, insider_id, transactiontype_code):
    obj = find(session, insider_id, transactiontype_code, last_date)
    if obj:
        return obj
    return save(
        session, last_date, shares_traded, last_price,
        shares_held, insider_id, transactiontype_code)
