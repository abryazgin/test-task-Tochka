import pytest

import parsers


@pytest.mark.parametrize("symbol, max_page_number", [
    ('CVX', 7),
    ('AAPL', 18),
    ('GOOG', 40),
])
def test_success_parse_tz_symbols(symbol, max_page_number):
    parser = parsers.parse_trade(symbol, page=1)
    rows = list(parser)
    assert len(rows)
    for row in rows:
        assert row.insider
        assert row.relation
        assert row.last_date
        assert row.transaction_type
        assert row.ownertype
        assert row.shares_traded is not None
        assert hasattr(row, 'last_price')  # last_price nullable
        assert row.shares_held is not None
    assert parser.get_max_page_number() == max_page_number
