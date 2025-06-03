import pytest
import requests
from unittest.mock import Mock, patch

from src.services.historical_price_error_handler import HistoricalPriceErrorHandler
from src.exceptions.historical_price_exceptions import (
    NetworkError, 
    RateLimitError, 
    DataNotFoundError, 
    InvalidParameterError
)

class TestHistoricalPriceErrorHandler:
    @patch('requests.get')
    def test_network_error_handling(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Network is unreachable")
        
        @HistoricalPriceErrorHandler.handle_error
        def mock_retrieval_method():
            requests.get("https://example.com")
        
        with pytest.raises(NetworkError):
            mock_retrieval_method(max_retries=1)
    
    @patch('requests.get')
    def test_rate_limit_handling(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '2'}
        
        mock_get.side_effect = [
            requests.exceptions.HTTPError(response=mock_response),
            Mock(status_code=200)
        ]
        
        @HistoricalPriceErrorHandler.handle_error
        def mock_retrieval_method():
            return requests.get("https://example.com")
        
        result = mock_retrieval_method(max_retries=2)
        assert result.status_code == 200
    
    @patch('requests.get')
    def test_data_not_found_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        
        mock_get.side_effect = requests.exceptions.HTTPError(response=mock_response)
        
        @HistoricalPriceErrorHandler.handle_error
        def mock_retrieval_method():
            requests.get("https://example.com")
        
        with pytest.raises(DataNotFoundError):
            mock_retrieval_method(max_retries=1)
    
    @patch('requests.get')
    def test_invalid_parameter_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 400
        
        mock_get.side_effect = requests.exceptions.HTTPError(response=mock_response)
        
        @HistoricalPriceErrorHandler.handle_error
        def mock_retrieval_method():
            requests.get("https://example.com")
        
        with pytest.raises(InvalidParameterError):
            mock_retrieval_method(max_retries=1)