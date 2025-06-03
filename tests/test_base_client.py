import pytest
import requests
import requests_mock
import aiohttp
from src.base_client import BaseAPIClient
from src.coingecko_api.base_client import CoinGeckoBaseClient, BaseAPIConfig

# Synchronous BaseAPIClient Tests
def test_base_client_initialization():
    """Test BaseAPIClient initialization."""
    base_url = "https://api.example.com"
    client = BaseAPIClient(base_url)
    
    assert client.base_url == base_url
    assert client.timeout == 10
    assert client.logger is not None

def test_successful_get_request():
    """Test a successful GET request."""
    base_url = "https://api.example.com"
    client = BaseAPIClient(base_url)
    
    with requests_mock.Mocker() as m:
        mock_response = {"data": "test"}
        m.get(f"{base_url}/test_endpoint", json=mock_response, status_code=200)
        
        result = client._make_request("GET", "test_endpoint")
        assert result == mock_response

def test_request_timeout():
    """Test request timeout handling."""
    base_url = "https://api.example.com"
    client = BaseAPIClient(base_url, timeout=1)
    
    with requests_mock.Mocker() as m:
        m.get(f"{base_url}/timeout_endpoint", exc=requests.exceptions.Timeout)
        
        with pytest.raises(RuntimeError, match="timed out"):
            client._make_request("GET", "timeout_endpoint")

def test_http_error_handling():
    """Test HTTP error handling."""
    base_url = "https://api.example.com"
    client = BaseAPIClient(base_url)
    
    with requests_mock.Mocker() as m:
        m.get(f"{base_url}/error_endpoint", status_code=404)
        
        with pytest.raises(RuntimeError, match="HTTP error"):
            client._make_request("GET", "error_endpoint")

def test_request_with_params():
    """Test request with query parameters."""
    base_url = "https://api.example.com"
    client = BaseAPIClient(base_url)
    
    with requests_mock.Mocker() as m:
        mock_response = {"data": "test"}
        m.get(f"{base_url}/params_endpoint", json=mock_response, status_code=200)
        
        result = client._make_request("GET", "params_endpoint", params={"key": "value"})
        assert result == mock_response

# Asynchronous CoinGecko Base Client Tests
@pytest.mark.asyncio
async def test_coingecko_base_client_initialization():
    """Test CoinGecko base client initialization."""
    async with CoinGeckoBaseClient() as client:
        assert client is not None

@pytest.mark.asyncio
async def test_coingecko_base_client_config():
    """Test CoinGecko client configuration."""
    config = BaseAPIConfig(base_url="https://test.api.com", timeout=5, retries=2)
    client = CoinGeckoBaseClient(config)
    assert client._config.base_url == "https://test.api.com"
    assert client._config.timeout == 5
    assert client._config.retries == 2

@pytest.mark.skip(reason="Requires actual API access")
@pytest.mark.asyncio
async def test_coingecko_base_client_request():
    """Placeholder for CoinGecko client request test."""
    async with CoinGeckoBaseClient() as client:
        # Simulate a request
        pass