class HistoricalPriceError(Exception):
    """Base exception for historical price retrieval errors."""
    pass

class NetworkError(HistoricalPriceError):
    """Raised when there's a network connectivity issue."""
    def __init__(self, message="Network error occurred during historical price retrieval"):
        self.message = message
        super().__init__(self.message)

class RateLimitError(HistoricalPriceError):
    """Raised when API rate limit is exceeded."""
    def __init__(self, message="API rate limit exceeded", retry_after=None):
        self.message = message
        self.retry_after = retry_after
        super().__init__(self.message)

class DataNotFoundError(HistoricalPriceError):
    """Raised when requested historical price data is not available."""
    def __init__(self, coin_id=None, date=None, message=None):
        self.coin_id = coin_id
        self.date = date
        self.message = message or f"Historical price data not found for {coin_id} on {date}"
        super().__init__(self.message)

class InvalidParameterError(HistoricalPriceError):
    """Raised when invalid parameters are provided for historical price retrieval."""
    def __init__(self, parameter=None, message=None):
        self.parameter = parameter
        self.message = message or f"Invalid parameter: {parameter}"
        super().__init__(self.message)