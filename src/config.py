import os
from typing import Optional
from dotenv import load_dotenv

class ConfigurationError(Exception):
    """Custom exception for configuration-related errors."""
    pass

def load_coingecko_config() -> dict:
    """
    Load CoinGecko API configuration from environment variables.
    
    Loads .env file and retrieves CoinGecko API credentials.
    
    Returns:
        dict: A dictionary containing CoinGecko API configuration.
    
    Raises:
        ConfigurationError: If required environment variables are missing or invalid.
    """
    # Load .env file (if it exists)
    load_dotenv()
    
    # Retrieve API key and optional configuration
    api_key = os.getenv('COINGECKO_API_KEY')
    api_base_url = os.getenv('COINGECKO_API_BASE_URL', 'https://api.coingecko.com/api/v3')
    
    # Validate required configuration
    if not api_key:
        raise ConfigurationError("COINGECKO_API_KEY environment variable is required.")
    
    return {
        'api_key': api_key,
        'base_url': api_base_url
    }