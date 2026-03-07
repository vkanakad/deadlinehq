"""Logging configuration for DeadlineHQ."""
import logging
import os
from datetime import datetime


def setup_logger(name: str = 'deadlinehq', log_file: str = None, level: int = logging.INFO) -> logging.Logger:
    """Set up and configure a logger.
    
    Args:
        name: Logger name
        log_file: Optional log file path (defaults to logs/deadlinehq_YYYYMMDD.log)
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    # Default log file with date
    if log_file is None:
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(log_dir, f'deadlinehq_{date_str}.log')
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler (only for WARNING and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger


# Global logger instance
_logger = None


def get_logger() -> logging.Logger:
    """Get or create the global logger instance.
    
    Returns:
        Logger instance
    """
    global _logger
    if _logger is None:
        _logger = setup_logger()
    return _logger
