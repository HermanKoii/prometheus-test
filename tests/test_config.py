import os
import pytest
from src.config import CoinGeckoConfig, ConfigurationError

def test_default_configuration():
    """Test default configuration loading."""
    config = CoinGeckoConfig()
    cfg = config.get_config()
    
    assert cfg['base_url'] == 'https://api.coingecko.com/api/v3'
    assert cfg['timeout'] == 10
    assert cfg['api_key'] is None

def test_env_variable_configuration(monkeypatch):
    """Test configuration loading from environment variables."""
    monkeypatch.setenv('COINGECKO_BASE_URL', 'https://custom-api.com')
    monkeypatch.setenv('COINGECKO_API_KEY', 'test_key')
    monkeypatch.setenv('COINGECKO_API_TIMEOUT', '30')

    config = CoinGeckoConfig()
    cfg = config.get_config()

    assert cfg['base_url'] == 'https://custom-api.com'
    assert cfg['timeout'] == 30
    assert cfg['api_key'] is not None

def test_manual_override_configuration():
    """Test manual configuration override."""
    config = CoinGeckoConfig(
        base_url='https://override-api.com',
        api_key='manual_key',
        timeout=15
    )
    cfg = config.get_config()

    assert cfg['base_url'] == 'https://override-api.com'
    assert cfg['timeout'] == 15
    assert cfg['api_key'] is not None

def test_invalid_timeout_cases():
    """Test handling of various invalid timeout scenarios."""
    invalid_cases = [
        '',         # Empty string
        '   ',      # Whitespace
        'invalid',  # Non-numeric string
        '-10',      # Negative number
        '0',        # Zero
        [],         # List
        {},         # Dictionary
        None,       # None
        float('nan'),  # Not a number
        float('inf')   # Infinity
    ]

    for case in invalid_cases:
        with pytest.raises(ConfigurationError, match="Invalid timeout value"):
            CoinGeckoConfig(timeout=case)

def test_float_timeout_conversion():
    """Test that float timeouts are converted to integers."""
    config = CoinGeckoConfig(timeout=15.7)
    cfg = config.get_config()
    assert cfg['timeout'] == 15

def test_from_dict_configuration():
    """Test configuration from dictionary."""
    config_dict = {
        'base_url': 'https://test-api.com',
        'api_key': 'test_key',
        'timeout': 20
    }
    config = CoinGeckoConfig.from_dict(config_dict)
    cfg = config.get_config()

    assert cfg['base_url'] == 'https://test-api.com'
    assert cfg['timeout'] == 20