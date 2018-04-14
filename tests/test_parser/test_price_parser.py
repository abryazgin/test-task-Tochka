import pytest

import parsers


@pytest.mark.parametrize("symbol", [
    'CVX',
    'AAPL',
    'GOOG',
])
def test_success_parse_tz_symbols(symbol):
    rows = list(parsers.parse_prices(symbol))
    assert len(rows)
    for row in rows:
        assert row.date
        assert row.open is not None
        assert row.high is not None
        assert row.low is not None
        assert row.close is not None
        assert row.volume is not None
