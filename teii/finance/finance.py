""" Finance Client classes """


import json
import logging
import os
import pandas as pd
import requests

from abc import ABC, abstractclassmethod, abstractmethod
from pathlib import Path
from typing import Optional, Union

from teii.finance import FinanceClientInvalidAPIKey
from teii.finance import FinanceClientAPIError
from teii.finance import FinanceClientInvalidData
from teii.finance import FinanceClientIOError


class FinanceClient(ABC):
    """ Wrapper around the Finance API. """

    _FinanceBaseQueryURL = "https://www.alphavantage.co/query?"  # Class variable

    def __init__(self, ticker: str,
                 api_key: Optional[str] = None,
                 logging_level: Union[int, str] = logging.WARNING,
                 logging_file: Optional[str] = None) -> None:
        """ FinanceClient constructor. """

        self._ticker = ticker
        self._api_key = api_key

        # Logging configuration
        self._setup_logging(logging_level, logging_file)

        # Finance API key configuration
        self._logger.info("API key configuration")
        if not self._api_key:
            self._api_key = os.getenv("TEII_FINANCE_API_KEY")
        if not self._api_key or not isinstance(self._api_key, str):
            raise FinanceClientInvalidAPIKey(f"{self.__class__.__qualname__} operation failed")

        # Query Finance API
        self._logger.info("Finance API access...")
        response = self._query_api()

        # Process query response
        self._logger.info("Finance API query response processing...")
        self._process_query_response(response)

        # Validate query data
        self._logger.info("Finance API query data validation...")
        self._validate_query_data()

        # Panda's Data Frame
        self._data_frame = None

    def _setup_logging(self,
                       logging_level: Union[int, str],
                       logging_file: Optional[str]) -> None:
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging_level)

    @classmethod
    def _build_base_query_url(cls) -> str:
        """Return base query URL.

        URL is independent from the query type.
            https://www.alphavantage.co/documentation/
        URL format:
            https://www.alphavantage.co/query?PARAMS
        """

        return cls._FinanceBaseQueryURL

    @abstractmethod
    def _build_base_query_url_params(self) -> str:
        """ Return base query URL parameters.

        Parameters are dependent on the query type:
            https://www.alphavantage.co/documentation/
        URL format:
            https://www.alphavantage.co/query?PARAMS
        """

        pass

    def _query_api(self) -> requests.Response:
        """ Query API endpoint. """

        try:
            response = requests.get(f"{self.__class__._build_base_query_url()}{self._build_base_query_url_params()}")
            assert response.status_code == 200
        except Exception as e:
            raise FinanceClientAPIError(f"Unsuccessful API access "
                                        f"[URL: {response.url}, status: {response.status_code}]") from e
        else:
            self._logger.info(f"Successful API access "
                              f"[URL: {response.url}, status: {response.status_code}]")
        return response

    @classmethod
    def _build_query_metadata_key(cls) -> str:
        """ Return metadata query key. """

        return "Meta Data"

    @abstractclassmethod
    def _build_query_data_key(cls) -> str:
        """ Return data query key. """

        pass

    def _process_query_response(self, response: requests.Response) -> None:
        """ Preprocess query data. """

        try:
            json_data_downloaded = response.json()
            self._json_metadata = json_data_downloaded[self._build_query_metadata_key()]
            self._json_data = json_data_downloaded[self._build_query_data_key()]
        except Exception as e:
            raise FinanceClientInvalidData("Invalid data") from e
        else:
            self._logger.info("Metadata and data fields found")

        self._logger.info(f"Metadata: '{self._json_metadata}'")
        self._logger.info(f"Data: '{json.dumps(self._json_data)[0:218]}...'")

    @abstractmethod
    def _validate_query_data(self) -> None:
        """ Validate query data. """

        pass

    def to_pandas(self) -> pd.DataFrame:
        """ Return pandas data frame from json data. """

        assert self._data_frame is not None

        return self._data_frame

    def to_csv(self, path2file: Path) -> Path:
        """ Write json data into csv file 'path2file'. """

        assert self._data_frame is not None

        try:
            self._data_frame.to_csv(path2file)
        except (IOError, PermissionError) as e:
            raise FinanceClientIOError(f"Unable to write json data into file '{path2file}'") from e

        return path2file
