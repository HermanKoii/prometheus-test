import os
import pytest
from src.coingecko_config import CoinGeckoConfig, CoinGeckoConfigValidationError

def test_default_configuration():
    config = CoinGeckoConfig()
    assert config.base_url == "https://api.coingecko.com/api/v3"
    assert config.timeout == 10
    assert config.cache_enabled is True
    assert config.cache_ttl == 300

def test_custom_configuration():
    config = CoinGeckoConfig(
        base_url="https://custom-api.coingecko.com",
        timeout=30,
        cache_enabled=False,
        cache_ttl=600
    )
    assert config.base_url == "https://custom-api.coingecko.com"
    assert config.timeout == 30
    assert config.cache_enabled is False
    assert config.cache_ttl == 600

def test_invalid_base_url():
    with pytest.raises(CoinGeckoConfigValidationError):
        CoinGeckoConfig(base_url="invalid_url")

def test_invalid_timeout():
    with pytest.raises(Exception):  # This will raise a validation error
        CoinGeckoConfig(timeout=-1)

def test_env_configuration(monkeypatch):
    monkeypatch.setenv('COINGECKO_BASE_URL', 'https://test-api.coingecko.com')
    monkeypatch.setenv('COINGECKO_TIMEOUT', '20')
    monkeypatch.setenv('COINGECKO_CACHE_ENABLED', 'false')
    monkeypatch.setenv('COINGECKO_CACHE_TTL', '900')

    config = CoinGeckoConfig.from_env()
    
    assert config.base_url == 'https://test-api.coingecko.com'
    assert config.timeout == 20
    assert config.cache_enabled is False
    assert config.cache_ttl == 900

def test_to_dict():
    config = CoinGeckoConfig()
    config_dict = config.to_dict()
    
    assert isinstance(config_dict, dict)
    assert config_dict['base_url'] == "https://api.coingecko.com/api/v3"
    assert config_dict['timeout'] == 10
    assert config_dict['cache_enabled'] is True