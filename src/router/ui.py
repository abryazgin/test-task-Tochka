from flask import render_template

import validator
import controllers as ctl
from main import app

from .utils import get_arg


@app.route('/')
def index():
    return render_template(
        'company/list.html',
        companies=ctl.company.list_all())


@app.route('/<company_code>')
def prices(company_code):
    company, prices_ = ctl.stockprice.list_last(company_code=company_code)
    return render_template(
        'company/index.html',
        with_prices=True,
        company=company.code,
        prices=prices_)


@app.route('/<company_code>/insider')
def trades(company_code):
    company, trades_ = ctl.stockinsidertrade.list_all(
        company_code=company_code)
    return render_template(
        'company/index.html',
        with_trades=True,
        company=company,
        trades=trades_)


@app.route('/<company_code>/insider/<insider_name>')
def trades_insider(company_code, insider_name):
    company, trades_ = ctl.stockinsidertrade.list_all(
        company_code=company_code, insider_name=insider_name)
    return render_template(
        'company/index.html',
        with_trades=True,
        company=company,
        trades=trades_)


@app.route('/<company_code>/analytics')
def price_delta(company_code):
    date_from = get_arg('date_from', type_=validator.to_date)
    date_to = get_arg('date_to', type_=validator.to_date)

    company, prices_ = ctl.stockprice.list_deltas(
        company_code=company_code, from_date=date_from, to_date=date_to)
    return render_template(
        'company/index.html',
        with_prices=True,
        company=company.code,
        prices=prices_)


@app.route('/<company_code>/delta')
def price_delta_intervals(company_code):
    value = get_arg('value', type_=float, required=True)
    price_type = get_arg('type', type_=validator.to_price_type, required=True)

    company, intervals = ctl.stockprice.get_minimal_delta_intervals(
        company_code=company_code, delta=value, price_type=price_type)
    return render_template(
        'company/index.html',
        with_intervals=True,
        company=company.code,
        intervals=intervals)
