"""
Unit tests for configuration exceptions.
"""

import pytest
from src.coingecko_client.config.exceptions import (
    ConfigurationError,
    InvalidConfigurationError,
    MissingConfigurationError,
    ConfigurationLoadError
)

def test_configuration_error():
    """Test base ConfigurationError."""
    with pytest.raises(ConfigurationError):
        raise ConfigurationError("Test error")

def test_invalid_configuration_error():
    """Test InvalidConfigurationError with and without config key."""
    error1 = InvalidConfigurationError("Invalid config")
    assert str(error1) == "Configuration Error: Invalid config"

    error2 = InvalidConfigurationError("Invalid value", "api_key")
    assert str(error2) == "Configuration Error for api_key: Invalid value"
    assert error2.config_key == "api_key"

def test_missing_configuration_error():
    """Test MissingConfigurationError."""
    error = MissingConfigurationError("base_url")
    assert str(error) == "Configuration Error for base_url: Required configuration parameter 'base_url' is missing"
    assert error.config_key == "base_url"

def test_configuration_load_error():
    """Test ConfigurationLoadError with and without original error."""
    original_error = ValueError("Test value error")
    error1 = ConfigurationLoadError("env_file")
    error2 = ConfigurationLoadError("env_file", original_error)

    assert str(error1) == "Failed to load configuration from env_file"
    assert str(error2) == "Failed to load configuration from env_file: Test value error"
    assert error2.source == "env_file"
    assert error2.original_error == original_error