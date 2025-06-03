import os
import json
import tempfile
import pytest
from src.config import load_config, ConfigurationError

def test_load_config_from_env():
    try:
        os.environ['COINGECKO_API_KEY'] = 'test_api_key'
        config = load_config()
        assert config['api_key'] == 'test_api_key'
    finally:
        os.environ.pop('COINGECKO_API_KEY', None)

def test_load_config_from_file():
    config_data = {
        'api_key': 'file_api_key',
        'max_retries': 5
    }
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_config:
        json.dump(config_data, temp_config)
        temp_config.close()
    
    try:
        config = load_config(temp_config.name)
        assert config['api_key'] == 'file_api_key'
        assert config['max_retries'] == 5
    finally:
        os.unlink(temp_config.name)

def test_load_config_default_values():
    config = load_config()
    assert config['base_url'] == 'https://api.coingecko.com/api/v3'
    assert config['timeout'] == 10
    assert config['max_retries'] == 3

def test_invalid_timeout():
    config_data = {'timeout': -1}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_config:
        json.dump(config_data, temp_config)
        temp_config.close()
    
    with pytest.raises(ConfigurationError):
        load_config(temp_config.name)
    
    os.unlink(temp_config.name)

def test_nonexistent_config_file():
    with pytest.raises(ConfigurationError):
        load_config('nonexistent_config.json')

def test_invalid_config_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_config:
        temp_config.write('invalid json')
        temp_config.close()
    
    with pytest.raises(ConfigurationError):
        load_config(temp_config.name)
    
    os.unlink(temp_config.name)