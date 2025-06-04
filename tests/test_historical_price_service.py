"""
Unit tests for HistoricalPriceService.

Test comprehensive error handling scenarios.
"""

import pytest
from unittest.mock import patch, Mock
import requests

from src.coingecko.historical_price_service import HistoricalPriceService
from src.coingecko.exceptions import (
    HistoricalPriceRetrievalError,
    RateLimitError,
    DataNotFoundError,
    NetworkError
)

@pytest.fixture
def historical_price_service():
    """Create a HistoricalPriceService instance for testing."""
    return HistoricalPriceService()

def test_valid_input_validation(historical_price_service):
    """Test input validation works correctly for valid inputs."""
    try:
        historical_price_service._validate_inputs(
            coin_id='bitcoin', 
            date='01-01-2023', 
            currency='usd'
        )
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")

def test_invalid_coin_id(historical_price_service):
    """Test validation fails for invalid coin ID."""
    with pytest.raises(ValueError, match="Invalid coin ID"):
        historical_price_service._validate_inputs(
            coin_id='', 
            date='01-01-2023', 
            currency='usd'
        )

def test_invalid_date_format(historical_price_service):
    """Test validation fails for incorrectly formatted date."""
    with pytest.raises(ValueError, match="Invalid date format"):
        historical_price_service._validate_inputs(
            coin_id='bitcoin', 
            date='2023-01-01', 
            currency='usd'
        )

@patch('requests.get')
def test_rate_limit_handling(mock_get, historical_price_service):
    """Test handling of API rate limit errors."""
    mock_response = Mock()
    mock_response.status_code = 429
    mock_get.return_value = mock_response

    with pytest.raises(RateLimitError, match="API rate limit exceeded"):
        historical_price_service.get_historical_price(
            coin_id='bitcoin', 
            date='01-01-2023'
        )

@patch('requests.get')
def test_data_not_found_handling(mock_get, historical_price_service):
    """Test handling of non-existent historical price data."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(DataNotFoundError, match="Historical price data not found"):
        historical_price_service.get_historical_price(
            coin_id='nonexistent_coin', 
            date='01-01-2023'
        )

@patch('requests.get')
def test_network_timeout(mock_get, historical_price_service):
    """Test handling of network timeout errors."""
    mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")

    with pytest.raises(NetworkError, match="Network error"):
        historical_price_service.get_historical_price(
            coin_id='bitcoin', 
            date='01-01-2023'
        )

@patch('requests.get')
def test_successful_price_retrieval(mock_get, historical_price_service):
    """Test successful historical price retrieval."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'market_data': {
            'current_price': {
                'usd': 50000.0
            }
        }
    }
    mock_get.return_value = mock_response

    price = historical_price_service.get_historical_price(
        coin_id='bitcoin', 
        date='01-01-2023'
    )
    assert price == 50000.0