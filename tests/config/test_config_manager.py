"""
Unit tests for configuration manager.
"""

import os
import pytest
from src.coingecko_client.config.manager import ConfigurationManager
from src.coingecko_client.config.exceptions import (
    MissingConfigurationError,
    InvalidConfigurationError,
    ConfigurationLoadError
)

def test_config_manager_default_values(monkeypatch):
    """Test default configuration values."""
    monkeypatch.delenv('COINGECKO_BASE_URL', raising=False)
    config = ConfigurationManager()

    assert config.get('base_url') == 'https://api.coingecko.com/api/v3'
    assert config.get('timeout') == 10.0
    assert config.get('max_retries') == 3

def test_config_manager_override():
    """Test configuration override."""
    config = ConfigurationManager(override_config={
        'base_url': 'https://custom-url.com',
        'timeout': 5.0
    })

    assert config.get('base_url') == 'https://custom-url.com'
    assert config.get('timeout') == 5.0

def test_config_manager_env_variables(monkeypatch):
    """Test loading configuration from environment variables."""
    monkeypatch.setenv('COINGECKO_BASE_URL', 'https://env-url.com')
    monkeypatch.setenv('COINGECKO_TIMEOUT', '15')
    monkeypatch.setenv('COINGECKO_MAX_RETRIES', '5')

    config = ConfigurationManager()

    assert config.get('base_url') == 'https://env-url.com'
    assert config.get('timeout') == 15.0
    assert config.get('max_retries') == 5

def test_config_manager_key_access():
    """Test dictionary-style configuration access."""
    config = ConfigurationManager(override_config={
        'base_url': 'https://test-url.com'
    })

    assert config['base_url'] == 'https://test-url.com'

    with pytest.raises(KeyError):
        _ = config['non_existent_key']

def test_config_manager_invalid_timeout():
    """Test invalid timeout configuration."""
    with pytest.raises(InvalidConfigurationError, match="Invalid timeout value"):
        ConfigurationManager(override_config={'timeout': -1})

def test_config_manager_missing_base_url():
    """Test missing base URL."""
    with pytest.raises(MissingConfigurationError, match="base_url"):
        ConfigurationManager(override_config={'base_url': ''})