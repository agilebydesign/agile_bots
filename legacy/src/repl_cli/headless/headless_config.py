import json
import os
from pathlib import Path
from typing import Optional


SECRETS_DIR = Path(__file__).parent.parent.parent.parent.parent.parent / 'secrets'
API_KEY_FILE = SECRETS_DIR / 'cursor_api_key.txt'
CONFIG_FILE = SECRETS_DIR / 'headless_config.json'


class HeadlessConfig:
    
    def __init__(self, api_key: str, log_dir: Optional[Path] = None):
        self.api_key = api_key
        self.log_dir = log_dir or Path('logs')
    
    @classmethod
    def load(cls) -> 'HeadlessConfig':
        api_key = cls._loads_api_key()
        log_dir = cls._loads_log_dir()
        return cls(api_key=api_key, log_dir=log_dir)
    
    @classmethod
    def _loads_api_key(cls) -> str:
        env_key = os.getenv('CURSOR_API_KEY')
        if env_key:
            return env_key
        
        if API_KEY_FILE.exists():
            return API_KEY_FILE.read_text().strip()
        
        if CONFIG_FILE.exists():
            config_data = json.loads(CONFIG_FILE.read_text())
            return config_data.get('api_key', '')
        
        config_path_env = os.getenv('HEADLESS_CONFIG_PATH')
        if config_path_env:
            config_path = Path(config_path_env)
            if config_path.exists():
                config_data = json.loads(config_path.read_text())
                return config_data.get('api_key', '')
        
        return ''
    
    @classmethod
    def _loads_log_dir(cls) -> Path:
        if CONFIG_FILE.exists():
            config_data = json.loads(CONFIG_FILE.read_text())
            return Path(config_data.get('log_dir', 'logs'))
        
        config_path_env = os.getenv('HEADLESS_CONFIG_PATH')
        if config_path_env:
            config_path = Path(config_path_env)
            if config_path.exists():
                config_data = json.loads(config_path.read_text())
                return Path(config_data.get('log_dir', 'logs'))
        
        return Path('logs')
    
    @property
    def is_configured(self) -> bool:
        return bool(self.api_key) and self.api_key != 'YOUR_API_KEY_HERE'
    
    @property
    def api_key_prefix(self) -> str:
        if not self.api_key:
            return ''
        return self.api_key[:10] + '...' if len(self.api_key) > 10 else self.api_key
