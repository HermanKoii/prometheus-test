import os
import json
import pytest
from src.config import CoinGeckoConfig, ConfigurationError

def test_default_config():
    config = CoinGeckoConfig()
    assert config.base_url == "https://api.coingecko.com/api/v3"
    assert config.timeout == 30
    assert config.default_currency == "usd"

def test_config_with_custom_params():
    config = CoinGeckoConfig(
        base_url="https://test.coingecko.com",
        api_key="test_key",
        timeout=15,
        default_currency="eur"
    )
    assert config.base_url == "https://test.coingecko.com"
    assert config.api_key == "test_key"
    assert config.timeout == 15
    assert config.default_currency == "eur"

def test_invalid_timeout():
    with pytest.raises(ConfigurationError):
        CoinGeckoConfig(timeout=0)

def test_empty_base_url():
    with pytest.raises(ConfigurationError):
        CoinGeckoConfig(base_url="")

def test_from_env(monkeypatch):
    monkeypatch.setenv('COINGECKO_BASE_URL', 'https://custom.coingecko.com')
    monkeypatch.setenv('COINGECKO_API_KEY', 'env_api_key')
    monkeypatch.setenv('COINGECKO_TIMEOUT', '45')
    monkeypatch.setenv('COINGECKO_DEFAULT_CURRENCY', 'eur')

    config = CoinGeckoConfig.from_env()
    assert config.base_url == 'https://custom.coingecko.com'
    assert config.api_key == 'env_api_key'
    assert config.timeout == 45
    assert config.default_currency == 'eur'

def test_to_dict():
    config = CoinGeckoConfig(api_key="test_key")
    config_dict = config.to_dict()
    assert config_dict['api_key'] == "test_key"
    assert config_dict['base_url'] == "https://api.coingecko.com/api/v3"

def test_from_file(tmp_path):
    config_data = {
        "base_url": "https://test.coingecko.com",
        "api_key": "file_key",
        "timeout": 20,
        "default_currency": "eur"
    }
    config_file = tmp_path / "config.json"
    with open(config_file, 'w') as f:
        json.dump(config_data, f)

    config = CoinGeckoConfig.from_file(str(config_file))
    assert config.base_url == "https://test.coingecko.com"
    assert config.api_key == "file_key"
    assert config.timeout == 20
    assert config.default_currency == "eur"

def test_from_file_not_found():
    with pytest.raises(ConfigurationError):
        CoinGeckoConfig.from_file("non_existent_file.json")

def test_from_file_invalid_json(tmp_path):
    invalid_config_file = tmp_path / "invalid_config.json"
    with open(invalid_config_file, 'w') as f:
        f.write("Invalid JSON")

    with pytest.raises(ConfigurationError):
        CoinGeckoConfig.from_file(str(invalid_config_file))