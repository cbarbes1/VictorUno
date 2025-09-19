"""Utility functions for VictorUno."""

import logging
import asyncio
from typing import Any, Callable, TypeVar, Coroutine
from functools import wraps
from pathlib import Path
import json

T = TypeVar('T')

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO", log_file: Path = None) -> None:
    """Set up logging configuration."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Set up file handler if specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    logger.info(f"Logging configured at {level} level")


def async_retry(max_retries: int = 3, delay: float = 1.0):
    """Decorator to retry async functions."""
    def decorator(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
                    
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay * (2 ** attempt))  # Exponential backoff
            
            logger.error(f"All {max_retries} attempts failed for {func.__name__}")
            raise last_exception
        
        return wrapper
    return decorator


def safe_json_load(file_path: Path, default: Any = None) -> Any:
    """Safely load JSON file with fallback."""
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.warning(f"Error loading JSON from {file_path}: {e}")
    
    return default


def safe_json_save(data: Any, file_path: Path) -> bool:
    """Safely save data to JSON file."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {e}")
        return False


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and unit_index < len(size_units) - 1:
        size /= 1024.0
        unit_index += 1
    
    return f"{size:.1f} {size_units[unit_index]}"


def validate_url(url: str) -> bool:
    """Validate if a string is a valid URL."""
    import re
    
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None


async def run_in_thread(func: Callable[..., T], *args, **kwargs) -> T:
    """Run a synchronous function in a thread pool."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)


class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, calls_per_second: float = 1.0):
        """Initialize rate limiter."""
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_called = 0.0
    
    async def acquire(self):
        """Acquire permission to make a call."""
        import time
        
        now = time.time()
        time_passed = now - self.last_called
        
        if time_passed < self.min_interval:
            wait_time = self.min_interval - time_passed
            await asyncio.sleep(wait_time)
        
        self.last_called = time.time()


class AsyncContextManager:
    """Base class for async context managers."""
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


def get_mime_type(file_path: Path) -> str:
    """Get MIME type for a file."""
    import mimetypes
    
    mime_type, _ = mimetypes.guess_type(str(file_path))
    return mime_type or "application/octet-stream"


def clean_filename(filename: str) -> str:
    """Clean filename by removing/replacing invalid characters."""
    import re
    
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove multiple underscores
    filename = re.sub(r'_+', '_', filename)
    
    # Trim underscores from start and end
    filename = filename.strip('_')
    
    return filename or "unnamed_file"


def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    from urllib.parse import urlparse
    
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return ""