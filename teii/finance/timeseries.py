""" Time Series Finance Client classes """


import datetime as dt
import logging
import pandas as pd

from typing import Optional, Union

from teii.finance import FinanceClientInvalidData
from teii.finance import FinanceClientParamError
from teii.finance import FinanceClient


class TimeSeriesFinanceClient(FinanceClient):
    """ Wrapper around the AlphaVantage API for Time Series Weekly Adjusted.

        Source:
            https://www.alphavantage.co/documentation/ (TIME_SERIES_WEEKLY_ADJUSTED)
    """

    _data_field2name_type = {
            "1. open":                  ("open",     "float"),
            "2. high":                  ("high",     "float"),
            "3. low":                   ("low",      "float"),
            "4. close":                 ("close",    "float"),
            "5. adjusted close":        ("aclose",   "float"),
            "6. volume":                ("volume",   "int"),
            "7. dividend amount":       ("dividend", "float")
        }

    def __init__(self, ticker: str,
                 api_key: Optional[str] = None,
                 logging_level: Union[int, str] = logging.WARNING) -> None:
        """ TimeSeriesFinanceClient constructor. """

        super().__init__(ticker, api_key, logging_level)

        self._build_data_frame()

    def _build_data_frame(self) -> None:
        """ Build Panda's DataFrame and format data. """

        # TODO
        #   Comprueba que no se produce ningún error y genera excepción
        #   'FinanceClientInvalidData' en caso de error

        try:
            # Build Panda's data frame
            data_frame = pd.DataFrame.from_dict(self._json_data, orient='index', dtype=float)
        except Exception as e:
            raise FinanceClientInvalidData("DataFrame creation error") from e

        # Rename data fields
        data_frame = data_frame.rename(columns={key: name_type[0]
                                                for key, name_type in self._data_field2name_type.items()})

        # Set data field types
        data_frame = data_frame.astype(dtype={name_type[0]: name_type[1]
                                              for key, name_type in self._data_field2name_type.items()})

        # Set index type
        data_frame.index = data_frame.index.astype("datetime64[ns]")

        # Sort data
        self._data_frame = data_frame.sort_index(ascending=True)

    def _build_base_query_url_params(self) -> str:
        """ Return base query URL parameters.

        Parameters are dependent on the query type:
            https://www.alphavantage.co/documentation/
        URL format:
            https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=TICKER&outputsize=full&apikey=API_KEY&data_type=json
        """

        return f"function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={self._ticker}&outputsize=full&apikey={self._api_key}"

    @classmethod
    def _build_query_data_key(cls) -> str:
        """ Return data query key. """

        return "Weekly Adjusted Time Series"

    def _validate_query_data(self) -> None:
        """ Validate query data. """

        try:
            assert self._json_metadata["2. Symbol"] == self._ticker
        except Exception as e:
            raise FinanceClientInvalidData("Metadata field '2. Symbol' not found") from e
        else:
            self._logger.info(f"Metadata key '2. Symbol' = '{self._ticker}' found")

    def weekly_price(self,
                     from_date: Optional[dt.date] = None,
                     to_date: Optional[dt.date] = None) -> pd.Series:
        """ Return weekly close price from 'from_date' to 'to_date'. """

        assert self._data_frame is not None

        self._logger.info("Dataframe is valid")
        series = self._data_frame['aclose']

        if from_date is not None and to_date is not None and from_date > to_date:
            raise FinanceClientParamError("The dates are invalid")
        else:
            self._logger.info("weekly_price valid dates")

        # FIXME: type hint error
        if from_date is not None and to_date is not None:
            series = series.loc[from_date:to_date]   # type: ignore

        return series

    def weekly_volume(self,
                      from_date: Optional[dt.date] = None,
                      to_date: Optional[dt.date] = None) -> pd.Series:
        """ Return weekly volume from 'from_date' to 'to_date'. """

        assert self._data_frame is not None
        self._logger.info("Dataframe is valid")
        series = self._data_frame['volume']

        if from_date is not None and to_date is not None and from_date > to_date:
            raise FinanceClientParamError("The dates are invalid")
        else:
            self._logger.info("weekly_volume valid dates")

        # FIXME: type hint error
        if from_date is not None and to_date is not None:
            series = series.loc[from_date:to_date]   # type: ignore

        return series

    def yearly_dividends(self,
                         from_year: Optional[int] = None,
                         to_year: Optional[int] = None) -> pd.Series:
        """ Return yearly dividends 'from_year' to 'to_year'. """

        assert self._data_frame is not None
        self._logger.info("Dataframe is valid")
        series = self._data_frame.groupby(self._data_frame.index.year)
        series = series['dividend'].apply(pd.DataFrame).sum()
        series.index = pd.to_datetime(series.index, format='%Y')
        series = series.rename('dividend')

        if from_year is not None and to_year is not None and from_year > to_year:
            raise FinanceClientParamError("The dates are invalid")
        else:
            self._logger.info("yearly_dividends valid dates")

        if from_year is not None and to_year is not None:
            series = series.loc[from_year:to_year]

        return series

    def highest_weekly_variation(self,
                                 from_year: Optional[int] = None,
                                 to_year: Optional[int] = None) -> pd.Series:
        """ Calculate the date there was a greater variation in the price of the ticker """

        assert self._data_frame is not None
        self._logger.info("Dataframe is valid")
        series = self._data_frame

        if from_year is not None and to_year is not None and from_year > to_year:
            raise FinanceClientParamError("The dates are invalid")
        else:
            self._logger.info("highest_weekly_variation valid dates")

        if from_year is not None and to_year is not None:
            series = series.loc[from_year:to_year]

        series['diference'] = series['high'] - series['low']
        row = series[series['diference'] == series['diference'].max()][['high', 'low', 'diference']]
        row = row.to_records()
        tuple = (pd.to_datetime(row[0][0]), row[0][1].astype(float),
                 row[0][2].astype(float), row[0][3].astype(float))

        return tuple
