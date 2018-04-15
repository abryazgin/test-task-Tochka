import validator
from flask import jsonify
import controllers as ctl
from main import app

from .utils import get_arg


@app.route('/api')
def api_index():
    return jsonify(list(map(ctl.company.marshall, ctl.company.list_all())))


@app.route('/api/<company_code>')
def api_prices(company_code):
    company, prices_ = ctl.stockprice.list_last(company_code=company_code)
    return jsonify(dict(
        company=ctl.company.marshall(company),
        prices=list(map(ctl.stockprice.marshall, prices_))
    ))


@app.route('/api/<company_code>/insider')
def api_trades(company_code):
    company, trades_ = ctl.stockinsidertrade.list_all(
        company_code=company_code)
    return jsonify(dict(
        company=ctl.company.marshall(company),
        trades=list(map(ctl.stockinsidertrade.marshall, trades_))
    ))


@app.route('/api/<company_code>/insider/<insider_name>')
def api_trades_insider(company_code, insider_name):
    company, trades_ = ctl.stockinsidertrade.list_all(
        company_code=company_code, insider_name=insider_name)
    return jsonify(dict(
        company=ctl.company.marshall(company),
        trades=list(map(ctl.stockinsidertrade.marshall, trades_))
    ))


@app.route('/api/<company_code>/analytics')
def api_price_delta(company_code):
    date_from = get_arg('date_from', type_=validator.to_date)
    date_to = get_arg('date_to', type_=validator.to_date)

    company, prices_ = ctl.stockprice.list_deltas(
        company_code=company_code, from_date=date_from, to_date=date_to)
    return jsonify(dict(
        company=ctl.company.marshall(company),
        deltas=list(prices_)
    ))


@app.route('/api/<company_code>/delta')
def api_price_delta_intervals(company_code):
    value = get_arg('value', type_=float, required=True)
    price_type = get_arg('type', type_=validator.to_price_type, required=True)

    company, intervals = ctl.stockprice.get_minimal_delta_intervals(
        company_code=company_code, delta=value, price_type=price_type)
    return jsonify(dict(
        company=ctl.company.marshall(company),
        intervals=list(intervals)
    ))
