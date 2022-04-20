""" Exception classes """


class FinanceClientError(Exception):
    """FinanceClient exception base class.

    https://www.loggly.com/blog/exceptional-logging-of-exceptions-in-python/ (Transformer Pattern)
    """

    pass


class FinanceClientInvalidAPIKey(FinanceClientError):
    """
    Invalid finance API Key.
    """

    def __init__(self, message):
        super().__init__('%s: %s' % (self.__class__.__name__, message))


class FinanceClientAPIError(FinanceClientError):
    """
    Finance API access failure.
    """

    def __init__(self, message):
        super().__init__('%s: %s' % (self.__class__.__name__, message))


class FinanceClientInvalidData(FinanceClientError):
    """
    Finance API returned incomplete or malformed data.
    """

    def __init__(self, message):
        super().__init__('%s: %s' % (self.__class__.__name__, message))


class FinanceClientIOError(FinanceClientError):
    """
    Error reading or writing data file.
    """

    def __init__(self, message):
        super().__init__('%s: %s' % (self.__class__.__name__, message))
