import logging
import os
from typing import Optional

def setup_logger(
    name: str = 'coingecko_client', 
    log_level: int = logging.INFO, 
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return a logger with file and console handlers.
    
    Args:
        name (str): Name of the logger.
        log_level (int): Logging level.
        log_file (Optional[str]): Path to log file. If None, logs to console.
    
    Returns:
        Configured logger instance.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Clear any existing handlers to prevent duplicate logs
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Global logger instance
logger = setup_logger(log_file='logs/coingecko_client.log')