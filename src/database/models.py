from main import db


class Company(db.Model):
    """ Компании == Акции == Symbol == code """
    code = db.Column(db.String, primary_key=True)  # code == symbol


class StockPrice(db.Model):
    """ Цены на Акции """
    company_code = db.Column(db.String, db.ForeignKey(Company.code), primary_key=True)
    date = db.Column(db.Date, primary_key=True)

    high = db.Column(db.Numeric, nullable=False)
    low = db.Column(db.Numeric, nullable=False)
    open = db.Column(db.Numeric, nullable=False)
    close = db.Column(db.Numeric, nullable=False)
    volume = db.Column(db.Numeric, nullable=False)

    company = db.relationship("Company")


class RelationType(db.Model):
    """ Типы отношений (relation для insider) """
    code = db.Column(db.String, primary_key=True)


class OwnerType(db.Model):
    """ Типы собственности (ownertype для insider) """
    code = db.Column(db.String, primary_key=True)


class Insider(db.Model):
    """ Совладельцы компаний """
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False, unique=True)
    company_code = db.Column(db.String, db.ForeignKey(Company.code), nullable=False)
    relationtype_code = db.Column(db.String, db.ForeignKey(RelationType.code), nullable=False)
    ownertype_code = db.Column(db.String, db.ForeignKey(OwnerType.code), nullable=False)

    relationtype = db.relationship("RelationType")
    ownertype = db.relationship("OwnerType")


class TransactionType(db.Model):
    """ Типы транзакций """
    code = db.Column(db.String, primary_key=True)


class StockInsiderTrade(db.Model):
    """ Торговые операции совладельцев компаний """
    insider_id = db.Column(db.Integer, db.ForeignKey(Insider.id), nullable=False, primary_key=True)
    transactiontype_code = db.Column(db.String, db.ForeignKey(TransactionType.code), nullable=False, primary_key=True)
    last_date = db.Column(db.Date, nullable=False, primary_key=True)

    shares_traded = db.Column(db.Integer, nullable=False)
    last_price = db.Column(db.Numeric)
    shares_held = db.Column(db.Integer, nullable=False)

    transactiontype = db.relationship("TransactionType")
    insider = db.relationship("Insider")
