""" Unit tests for teii.finance subpackage """


import json
import pandas as pd
import unittest.mock as mock
import teii.finance.finance

from importlib import resources
from pytest import fixture


@fixture(scope='session')
def api_key_str():
    return ("nokey")


@fixture(scope='package')
def mocked_requests():
    def mocked_get(url):
        response = mock.Mock()
        response.status_code = 200
        if 'IBM' in url:
            json_filename = 'TIME_SERIES_WEEKLY_ADJUSTED.IBM.json'
        elif 'NODATA' in url:
            json_filename = 'NODATA.json'
        else:
            raise ValueError('Ticker no soportado')
        with resources.open_text('teii.finance.data', json_filename) as json_fid:
            json_data = json.load(json_fid)
        response.json.return_value = json_data
        return response

    requests = mock.Mock()
    requests.get.side_effect = mocked_get

    teii.finance.finance.requests = requests


@fixture(scope='package')
def pandas_series_IBM_prices():
    with resources.path('teii.finance.data', 'TIME_SERIES_WEEKLY_ADJUSTED.IBM.aclose.unfiltered.csv') as path2csv:
        df = pd.read_csv(path2csv, index_col=0, parse_dates=True)
        ds = df['aclose']
    return ds


@fixture(scope='package')
def pandas_series_IBM_prices_filtered():
    with resources.path('teii.finance.data', 'TIME_SERIES_WEEKLY_ADJUSTED.IBM.aclose.filtered.csv') as path2csv:
        df = pd.read_csv(path2csv, index_col=0, parse_dates=True)
        ds = df['aclose']
    return ds

@fixture(scope='package')
def pandas_series_IBM_volume():
    with resources.path('teii.finance.data', 'TIME_SERIES_WEEKLY_ADJUSTED.IBM.volume.unfiltered.csv') as path2csv:
        df = pd.read_csv(path2csv, index_col=0, parse_dates=True)
        ds = df['volume']
    return ds

@fixture(scope='package')
def pandas_series_IBM_volume_filtered():
    with resources.path('teii.finance.data', 'TIME_SERIES_WEEKLY_ADJUSTED.IBM.volume.filtered.csv') as path2csv:
        df = pd.read_csv(path2csv, index_col=0, parse_dates=True)
        ds = df['volume']
    return ds

@fixture(scope='package')
def pandas_series_IBM_yearly_dividends():
    with resources.path('teii.finance.data', 'TIME_SERIES_WEEKLY_ADJUSTED.IBM.yearly_dividend.unfiltered.csv') as path2csv:
        df = pd.read_csv(path2csv, index_col=0, parse_dates=True)
        ds = df['dividend']
    return ds

@fixture(scope='package')
def pandas_series_IBM_yearly_dividends_filtered():
    with resources.path('teii.finance.data', 'TIME_SERIES_WEEKLY_ADJUSTED.IBM.yearly_dividend.filtered.csv') as path2csv:
        df = pd.read_csv(path2csv, index_col=0, parse_dates=True)
        ds = df['dividend']
    return ds

@fixture(scope='package')
def tuple_highest_weekly_variation():
    date = '2020-03-13 00:00:00'
    date = pd.to_datetime(date)
    high = 124.88
    low = 100.81
    diff = 24.069999999999993
    tuple = (date,high,low,diff)
    return tuple

@fixture(scope='package')
def tuple_highest_weekly_variation_filtered():
    date = '2018-04-20 00:00:00'
    date = pd.to_datetime(date)
    high = 162.0
    low = 144.51
    diff = 17.49000000000001
    tuple = (date,high,low,diff)
    return tuple
