import os
import pytest
from src.config import load_coingecko_config, ConfigurationError

def test_load_coingecko_config_success(monkeypatch):
    """Test successful configuration loading."""
    monkeypatch.setenv('COINGECKO_API_KEY', 'test_api_key')
    monkeypatch.setenv('COINGECKO_API_BASE_URL', 'https://custom-api.com')
    
    config = load_coingecko_config()
    
    assert config['api_key'] == 'test_api_key'
    assert config['base_url'] == 'https://custom-api.com'

def test_load_coingecko_config_default_url(monkeypatch):
    """Test default base URL when not specified."""
    monkeypatch.setenv('COINGECKO_API_KEY', 'test_api_key')
    monkeypatch.delenv('COINGECKO_API_BASE_URL', raising=False)
    
    config = load_coingecko_config()
    
    assert config['api_key'] == 'test_api_key'
    assert config['base_url'] == 'https://api.coingecko.com/api/v3'

def test_load_coingecko_config_missing_key(monkeypatch):
    """Test configuration fails when API key is missing."""
    monkeypatch.delenv('COINGECKO_API_KEY', raising=False)
    
    with pytest.raises(ConfigurationError, match="COINGECKO_API_KEY environment variable is required."):
        load_coingecko_config()