import pytest
import requests
from unittest.mock import patch
from src.api_validator import CoinGeckoAPIValidator, CoinGeckoAPIConnectionError

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
    
    def json(self):
        return self.json_data

def test_successful_connection_validation():
    # Setup a mock response that simulates a successful API ping
    with patch('requests.get') as mock_get:
        mock_get.return_value = MockResponse(
            {'gecko_says': '(V3) To the Moon!'}, 
            200
        )
        
        validator = CoinGeckoAPIValidator()
        result = validator.validate_connection()
        
        assert result == {'gecko_says': '(V3) To the Moon!'}
        mock_get.assert_called_once()

def test_connection_network_error():
    # Test network connection failure
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Network Error")
        
        validator = CoinGeckoAPIValidator()
        
        with pytest.raises(CoinGeckoAPIConnectionError, 
                           match="Network error"):
            validator.validate_connection()

def test_connection_invalid_status_code():
    # Test non-200 status code handling
    with patch('requests.get') as mock_get:
        mock_get.return_value = MockResponse(
            {'error': 'Some error'}, 
            500
        )
        
        validator = CoinGeckoAPIValidator()
        
        with pytest.raises(CoinGeckoAPIConnectionError, 
                           match="API Connection failed"):
            validator.validate_connection()

def test_connection_unexpected_response():
    # Test unexpected response format
    with patch('requests.get') as mock_get:
        mock_get.return_value = MockResponse(
            {'unexpected': 'response'}, 
            200
        )
        
        validator = CoinGeckoAPIValidator()
        
        with pytest.raises(CoinGeckoAPIConnectionError, 
                           match="Unexpected API response format"):
            validator.validate_connection()