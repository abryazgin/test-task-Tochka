from database import models as md


def list_all():
    return iter(md.Company.query)


def get_or_save(session, code):
    """ Дай если есть. Если нет - создай и верни """
    obj = session.query(md.Company).get(code)
    if not obj:
        obj = md.Company(code=code)
        session.add(obj)
        session.flush()
    return obj


def marshall(obj):
    """ Маршализация """
    d = dict()
    d['code'] = obj.code
    return d
