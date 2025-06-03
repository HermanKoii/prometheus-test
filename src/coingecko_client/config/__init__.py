"""
Configuration package for CoinGecko API client.

Exports key configuration management classes and functions.
"""

from .manager import ConfigurationManager
from .exceptions import (
    ConfigurationError, 
    InvalidConfigurationError, 
    MissingConfigurationError, 
    ConfigurationLoadError
)
from .logging_config import setup_logging, get_logger

__all__ = [
    'ConfigurationManager',
    'ConfigurationError',
    'InvalidConfigurationError',
    'MissingConfigurationError',
    'ConfigurationLoadError',
    'setup_logging',
    'get_logger'
]