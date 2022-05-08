""" Unit tests for teii.finance.timeseries module """


import datetime as dt
import pytest

from pandas.testing import assert_series_equal

from teii.finance import TimeSeriesFinanceClient
from teii.finance import FinanceClientInvalidAPIKey
from teii.finance import FinanceClientInvalidData
from teii.finance import FinanceClientParamError


def test_constructor_success(api_key_str,
                             mocked_requests):
    TimeSeriesFinanceClient("IBM", api_key_str)


def test_constructor_failure_invalid_api_key():
    with pytest.raises(FinanceClientInvalidAPIKey):
        TimeSeriesFinanceClient("IBM")

def test_constructor_invalid_data(api_key_str,
                                 mocked_requests):
    with pytest.raises(FinanceClientInvalidData):
        TimeSeriesFinanceClient("NODATA", api_key_str)

def test_weekly_price_invalid_dates(api_key_str,
                                    mocked_requests):
    with pytest.raises(FinanceClientParamError):
        fc = TimeSeriesFinanceClient("IBM", api_key_str)

        fc.weekly_price(dt.date(year=2022, month=1, day=1),
                        dt.date(year=2021, month=12, day=31))


def test_weekly_price_no_dates(api_key_str,
                               mocked_requests,
                               pandas_series_IBM_prices):
    fc = TimeSeriesFinanceClient("IBM", api_key_str)

    ps = fc.weekly_price()

    assert ps.count() == 1162   # 1999-11-12 to 2022-02-11 (1162 business weeks)

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
    with pytest.raises(FinanceClientParamError):
        
        fc = TimeSeriesFinanceClient("IBM", api_key_str)
        fc.weekly_price(dt.date(year=2022, month=1, day=1),
                        dt.date(year=2021, month=12, day=31))

def test_weekly_volume_dates(api_key_str,
                             mocked_requests,
                             pandas_series_IBM_volume_filtered):

    fc = TimeSeriesFinanceClient("IBM", api_key_str)

    ps = fc.weekly_volume(dt.date(year=2019, month=1, day=1),
                          dt.date(year=2021, month=12, day=31))
    
    assert ps.count() == 157   # 2019-01-01 to 2021-12-31 (157 business weeks)

    assert ps.count() == pandas_series_IBM_volume_filtered.count()

    assert_series_equal(ps, pandas_series_IBM_volume_filtered)

def test_weekly_volume_no_dates(api_key_str,
                                mocked_requests,
                                pandas_series_IBM_volume):
    fc = TimeSeriesFinanceClient("IBM", api_key_str)

    ps = fc.weekly_volume()

    assert ps.count() == 1162    # 1999-11-12 to 2022-02-11 (1162 business weeks)

    assert ps.count() == pandas_series_IBM_volume.count()

    assert_series_equal(ps, pandas_series_IBM_volume)

def test_yearly_dividends_invalid_dates(api_key_str,
                                        mocked_requests):
    with pytest.raises(FinanceClientParamError):
        
        fc = TimeSeriesFinanceClient("IBM", api_key_str)
        fc.yearly_dividends(dt.date(year=2022, month=1, day=1),
                            dt.date(year=2021, month=12, day=31))

def test_yearly_dividends_no_dates(api_key_str,
                                   mocked_requests,
                                   pandas_series_IBM_yearly_dividends):
    fc = TimeSeriesFinanceClient("IBM", api_key_str)

    ps = fc.yearly_dividends()

    assert ps.count() == 24  # 1999-01-01 to 2022-01-01 (24 business years)

    assert ps.count() == pandas_series_IBM_yearly_dividends.count()

    assert_series_equal(ps,pandas_series_IBM_yearly_dividends)

def test_yearly_dividends_dates(api_key_str,
                                   mocked_requests,
                                   pandas_series_IBM_yearly_dividends_filtered):
    fc = TimeSeriesFinanceClient("IBM", api_key_str)

    ps = fc.yearly_dividends(dt.date(year=2015, month=1, day=1),
                             dt.date(year=2019, month=1, day=1))

    assert ps.count() == 5  # 2015-01-01 to 2019-01-01 (5 business years)

    assert ps.count() == pandas_series_IBM_yearly_dividends_filtered.count()

    assert_series_equal(ps,pandas_series_IBM_yearly_dividends_filtered)

def test_highest_weekly_variation_invalid_dates(api_key_str,
                                                 mocked_requests):
    with pytest.raises(FinanceClientParamError):

        fc = TimeSeriesFinanceClient("IBM", api_key_str)
        
        fc.highest_weekly_variation(dt.date(year=2022, month=1, day=1),
                                    dt.date(year=2021, month=12, day=31))

def test_highest_weekly_variation_dates(api_key_str,
                                             mocked_requests,
                                             tuple_highest_weekly_variation_filtered):

    fc = TimeSeriesFinanceClient("IBM", api_key_str)

    tuple = fc.highest_weekly_variation(dt.date(year=2015, month=1, day=1),
                                         dt.date(year=2019, month=12, day=31))

    assert tuple == tuple_highest_weekly_variation_filtered # cumple la salida del enunciado

def test_highest_weekly_variation_no_dates(api_key_str,
                                             mocked_requests,
                                             tuple_highest_weekly_variation):

    fc = TimeSeriesFinanceClient("IBM", api_key_str)

    tuple = fc.highest_weekly_variation()

    assert tuple == tuple_highest_weekly_variation # cumple la salida del enunciado




