"""Configuration management for DeadlineHQ."""
import json
import os
from typing import Any


class Config:
    """Configuration manager that loads settings from config file and environment variables."""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from file, with fallback to defaults."""
        default_config = {
            'email': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'sender_email': '',
                'use_env_password': True
            },
            'scheduler': {
                'daily_update_time': '09:00',
                'deadline_check_interval_hours': 1,
                'deadline_alert_threshold_days': 1
            },
            'storage': {
                'tasks_file': 'tasks.json',
                'backup_enabled': False,
                'backup_directory': 'backups'
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    self._deep_merge(default_config, loaded_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}. Using defaults.")
        
        return default_config
    
    def _deep_merge(self, base: dict, update: dict):
        """Recursively merge update dict into base dict."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get(self, *keys: str, default: Any = None) -> Any:
        """Get configuration value by nested keys.
        
        Args:
            *keys: Nested keys to traverse (e.g., 'email', 'smtp_server')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def get_email_password(self) -> str:
        """Get email password from environment variable.
        
        Returns:
            Email password from DEADLINEHQ_EMAIL_PASSWORD env var
            
        Raises:
            ValueError: If environment variable is not set
        """
        password = os.getenv('DEADLINEHQ_EMAIL_PASSWORD')
        if not password:
            raise ValueError(
                "Email password not found. Please set DEADLINEHQ_EMAIL_PASSWORD environment variable."
            )
        return password
    
    def get_sender_email(self) -> str:
        """Get sender email, preferring environment variable over config.
        
        Returns:
            Sender email address
        """
        env_email = os.getenv('DEADLINEHQ_SENDER_EMAIL')
        if env_email:
            return env_email
        return self.get('email', 'sender_email', default='')


# Global config instance
_config = None


def get_config(config_file: str = 'config.json') -> Config:
    """Get or create global config instance.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config(config_file)
    return _config
