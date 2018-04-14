import pytest

import parsers


@pytest.mark.parametrize("symbol", [
    'CVX',
    'AAPL',
    'GOOG',
])
def test_success_parse_tz_symbols(symbol):
    rows = list(parsers.parse_trade(symbol))
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
