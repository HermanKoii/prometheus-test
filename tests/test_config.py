import os
import pytest
from src.config import load_config, ConfigurationError


def test_default_config(monkeypatch):
    """Test default configuration loading."""
    monkeypatch.delenv('COINGECKO_API_BASE_URL', raising=False)
    monkeypatch.delenv('COINGECKO_API_KEY', raising=False)
    monkeypatch.delenv('COINGECKO_REQUEST_TIMEOUT', raising=False)
    monkeypatch.delenv('COINGECKO_MAX_RETRIES', raising=False)
    monkeypatch.delenv('COINGECKO_RATE_LIMIT_DELAY', raising=False)

    config = load_config()
    assert config['api_base_url'] == 'https://api.coingecko.com/api/v3'
    assert config['api_key'] == ''
    assert config['request_timeout'] == 30
    assert config['max_retries'] == 3
    assert config['rate_limit_delay'] == 1


def test_custom_config(monkeypatch):
    """Test loading custom configuration from environment variables."""
    monkeypatch.setenv('COINGECKO_API_BASE_URL', 'https://custom-api.com')
    monkeypatch.setenv('COINGECKO_API_KEY', 'test_key')
    monkeypatch.setenv('COINGECKO_REQUEST_TIMEOUT', '60')
    monkeypatch.setenv('COINGECKO_MAX_RETRIES', '5')
    monkeypatch.setenv('COINGECKO_RATE_LIMIT_DELAY', '2')

    config = load_config()
    assert config['api_base_url'] == 'https://custom-api.com'
    assert config['api_key'] == 'test_key'
    assert config['request_timeout'] == 60
    assert config['max_retries'] == 5
    assert config['rate_limit_delay'] == 2


def test_invalid_timeout_config(monkeypatch):
    """Test configuration validation for negative timeout."""
    monkeypatch.setenv('COINGECKO_REQUEST_TIMEOUT', '-10')

    with pytest.raises(ConfigurationError, match="Request timeout must be a positive integer"):
        load_config()


def test_empty_base_url_config(monkeypatch):
    """Test configuration validation for empty base URL."""
    monkeypatch.setenv('COINGECKO_API_BASE_URL', '')

    with pytest.raises(ConfigurationError, match="Invalid or missing API base URL"):
        load_config()


def test_negative_retries_config(monkeypatch):
    """Test configuration validation for negative retries."""
    monkeypatch.setenv('COINGECKO_MAX_RETRIES', '-3')

    with pytest.raises(ConfigurationError, match="Max retries cannot be negative"):
        load_config()