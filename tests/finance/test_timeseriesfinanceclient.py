""" Unit tests for teii.finance.timeseries module """


import datetime as dt
import pytest

from pandas.testing import assert_series_equal

from teii.finance import TimeSeriesFinanceClient
from teii.finance import FinanceClientInvalidAPIKey


def test_constructor_success(api_key_str,
                             mocked_requests):
    TimeSeriesFinanceClient("IBM", api_key_str)


def test_constructor_failure_invalid_api_key():
    with pytest.raises(FinanceClientInvalidAPIKey):
        TimeSeriesFinanceClient("IBM")


def test_weekly_price_invalid_dates(api_key_str,
                                    mocked_requests):
    # TODO
    pass


def test_weekly_price_no_dates(api_key_str,
                               mocked_requests,
                               pandas_series_IBM_prices):
    fc = TimeSeriesFinanceClient("IBM", api_key_str)

    ps = fc.weekly_price()

    assert ps.count() == 1162   # 2019-11-01 to 2022-02-11 (1162 business weeks)

    assert ps.count() == pandas_series_IBM_prices.count()

    assert_series_equal(ps, pandas_series_IBM_prices)


def test_weekly_price_dates(api_key_str,
                            mocked_requests,
                            pandas_series_IBM_prices_filtered):
    fc = TimeSeriesFinanceClient("IBM", api_key_str)

    ps = fc.weekly_price(dt.date(year=2019, month=1, day=1),
                         dt.date(year=2021, month=12, day=31))

    assert ps.count() == 157    # 2019-01-01 to 2021-12-31 (157 business weeks)

    assert ps.count() == pandas_series_IBM_prices_filtered.count()

    assert_series_equal(ps, pandas_series_IBM_prices_filtered)


def test_weekly_volume_invalid_dates(api_key_str,
                                     mocked_requests):
    # TODO
    pass


def test_weekly_volume_no_dates(api_key_str,
                                mocked_requests):
    # TODO
    pass


def test_weekly_volume_dates(api_key_str,
                             mocked_requests):
    # TODO
    pass
