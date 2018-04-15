from database import models as md


def get_or_save(session, code):
    """ Дай если есть. Если нет - создай и верни """
    obj = session.query(md.RelationType).get(code)
    if not obj:
        obj = md.RelationType(code=code)
        session.add(obj)
        session.flush()
    return obj

