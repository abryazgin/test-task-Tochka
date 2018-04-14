from database import models as md


def save(session, name, company_code, relationtype_code, ownertype_code):
    obj = md.Insider(
        name=name,
        company_code=company_code,
        relationtype_code=relationtype_code,
        ownertype_code=ownertype_code)
    session.add(obj)
    session.flush()
    return obj


def find(session, name):
    return session.query(md.Insider).filter_by(name=name).first()


def get_or_save(session, name, company_code, relationtype_code, ownertype_code):
    obj = find(session=session, name=name)
    if obj:
        return obj
    return save(
        session=session, name=name, company_code=company_code,
        relationtype_code=relationtype_code, ownertype_code=ownertype_code)
