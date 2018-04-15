from database import models as md


def list_all(company_code, insider_name=None):
    """
    Получение всех операций по акциям.
    """
    company = md.Company.query.get_or_404(company_code)
    insider = (
        md.Insider.query.filter(
            md.Insider.name == insider_name).filter(
            md.Insider.company_code == company_code).first_or_404()
        if insider_name
        else None)

    q = md.StockInsiderTrade.query.join(md.Insider).filter(
        md.Insider.company_code == company_code)
    if insider:
        q = q.filter(md.StockInsiderTrade.insider_id == insider.id)
    return company, iter(q)


def get_or_save(
        session, last_date, shares_traded, last_price,
        shares_held, insider_id, transactiontype_code):
    """ Дай если есть. Если нет - создай и верни """
    obj = session.query(md.StockInsiderTrade).filter_by(
        insider_id=insider_id, transactiontype_code=transactiontype_code,
        last_date=last_date).first()
    if not obj:
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


def marshall(obj):
    """ Маршализация """
    d = dict()
    d['insider'] = obj.insider.name
    d['relation'] = obj.insider.relationtype_code
    d['ownertype'] = obj.insider.ownertype_code
    d['transactiontype_code'] = obj.transactiontype_code
    d['last_date'] = obj.last_date
    d['shares_traded'] = obj.shares_traded
    d['last_price'] = obj.last_price
    d['shares_held'] = obj.shares_held
    return d
