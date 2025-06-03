"""
Logging configuration for the CoinGecko API client.

This module sets up a centralized logging configuration 
to provide consistent and comprehensive logging across the client.
"""

import logging
import os
from typing import Optional, Union

def setup_logging(
    log_level: Union[str, int] = logging.INFO, 
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configure and set up logging for the CoinGecko client.

    Args:
        log_level (Union[str, int], optional): Logging level. Defaults to logging.INFO.
        log_file (Optional[str], optional): Path to log file. Defaults to None.

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger('coingecko_client')
    logger.setLevel(log_level)

    # Clear any existing handlers to prevent duplicate logging
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        try:
            # Ensure log directory exists
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except (IOError, OSError) as e:
            logger.warning(f"Could not create log file {log_file}: {e}")

    return logger

def get_logger(name: str = 'coingecko_client') -> logging.Logger:
    """
    Get a logger for a specific module.

    Args:
        name (str, optional): Logger name. Defaults to 'coingecko_client'.

    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)