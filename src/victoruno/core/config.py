"""Configuration management for VictorUno."""

import os
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from pydantic import BaseModel, Field
    PYDANTIC_AVAILABLE = True
except ImportError:
    # Mock pydantic for testing
    class BaseModel:
        def __init__(self, **kwargs):
            # Set defaults from class annotations
            for attr_name in dir(self.__class__):
                if not attr_name.startswith('_'):
                    attr_value = getattr(self.__class__, attr_name)
                    if not callable(attr_value):
                        setattr(self, attr_name, attr_value)
            
            # Override with provided kwargs
            for key, value in kwargs.items():
                setattr(self, key, value)
        
        def model_dump(self):
            return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    def Field(default=None, description=""):
        return default
    
    PYDANTIC_AVAILABLE = False

try:
    from dotenv import load_dotenv
    # Load environment variables from .env file if it exists
    load_dotenv()
except ImportError:
    # Mock dotenv
    def load_dotenv():
        pass


class Config(BaseModel):
    """Configuration settings for VictorUno."""
    
    # Ollama settings
    ollama_host: str = Field(default="http://localhost:11434", description="Ollama server host")
    ollama_model: str = Field(default="llama2", description="Default Ollama model to use")
    
    # Agent settings
    agent_name: str = Field(default="VictorUno", description="Name of the agent")
    agent_description: str = Field(
        default="Personal agent for research, development, and optimization",
        description="Description of the agent"
    )
    
    # Web interface settings
    web_host: str = Field(default="0.0.0.0", description="Web interface host")
    web_port: int = Field(default=8000, description="Web interface port")
    
    # GUI settings
    gui_theme: str = Field(default="dark", description="GUI theme (dark/light)")
    gui_width: int = Field(default=1200, description="GUI window width")
    gui_height: int = Field(default=800, description="GUI window height")
    
    # Document processing
    max_file_size: int = Field(default=10 * 1024 * 1024, description="Maximum file size in bytes (10MB)")
    supported_formats: list[str] = Field(
        default=["pdf", "txt", "docx", "md"],
        description="Supported document formats"
    )
    
    # Chrome integration
    chrome_driver_path: Optional[str] = Field(default=None, description="Path to Chrome driver")
    chrome_headless: bool = Field(default=True, description="Run Chrome in headless mode")
    
    # Storage settings
    data_dir: Path = Field(default=Path.home() / ".victoruno", description="Data directory")
    documents_dir: Optional[Path] = Field(default=None, description="Documents directory")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set up directories
        if self.documents_dir is None:
            self.documents_dir = self.data_dir / "documents"
        
        # Create directories if they don't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.documents_dir.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        return cls(
            ollama_host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            ollama_model=os.getenv("OLLAMA_MODEL", "llama2"),
            agent_name=os.getenv("AGENT_NAME", "VictorUno"),
            web_host=os.getenv("WEB_HOST", "0.0.0.0"),
            web_port=int(os.getenv("WEB_PORT", "8000")),
            gui_theme=os.getenv("GUI_THEME", "dark"),
            chrome_driver_path=os.getenv("CHROME_DRIVER_PATH"),
            chrome_headless=os.getenv("CHROME_HEADLESS", "true").lower() == "true",
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self.model_dump()


# Global configuration instance
config = Config.from_env()