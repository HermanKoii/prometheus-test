"""
Custom exceptions for CoinGecko Client configuration errors.

This module defines a hierarchy of exceptions specifically for 
configuration-related errors in the CoinGecko API client.
"""

class ConfigurationError(Exception):
    """Base exception for configuration-related errors."""
    pass

class InvalidConfigurationError(ConfigurationError):
    """Raised when configuration parameters are invalid or incomplete."""
    def __init__(self, message: str, config_key: str = None):
        """
        Initialize the InvalidConfigurationError.

        Args:
            message (str): Detailed error message
            config_key (str, optional): The specific configuration key causing the error
        """
        self.config_key = config_key
        super().__init__(f"Configuration Error{f' for {config_key}' if config_key else ''}: {message}")

class MissingConfigurationError(InvalidConfigurationError):
    """Raised when a required configuration parameter is missing."""
    def __init__(self, missing_key: str):
        """
        Initialize the MissingConfigurationError.

        Args:
            missing_key (str): The name of the missing configuration key
        """
        super().__init__(f"Required configuration parameter '{missing_key}' is missing", missing_key)

class ConfigurationLoadError(ConfigurationError):
    """Raised when there is an error loading configuration from a source."""
    def __init__(self, source: str, original_error: Exception = None):
        """
        Initialize the ConfigurationLoadError.

        Args:
            source (str): The source of configuration (e.g., file path, environment)
            original_error (Exception, optional): The original error that occurred
        """
        error_msg = f"Failed to load configuration from {source}"
        if original_error:
            error_msg += f": {str(original_error)}"
        super().__init__(error_msg)
        self.source = source
        self.original_error = original_error