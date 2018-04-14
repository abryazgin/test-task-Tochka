from database import models as md


def save(session, code):
    obj = md.RelationType(code=code)
    session.add(obj)
    session.flush()
    return obj


def get(session, code):
    return session.query(md.RelationType).get(code)


def get_or_save(session, code):
    obj = get(session=session, code=code)
    if obj:
        return obj
    return save(session=session, code=code)

