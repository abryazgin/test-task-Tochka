from database import models as md


def get_or_save(session, name, company_code, relationtype_code, ownertype_code):
    """ Дай если есть. Если нет - создай и верни """
    obj = session.query(md.Insider).filter_by(name=name).first()
    if not obj:
        obj = md.Insider(
            name=name,
            company_code=company_code,
            relationtype_code=relationtype_code,
            ownertype_code=ownertype_code)
        session.add(obj)
        session.flush()
    return obj
