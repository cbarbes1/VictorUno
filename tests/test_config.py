"""Test configuration for VictorUno."""

import pytest
import os
import tempfile
from pathlib import Path

from victoruno.core.config import Config


def test_config_defaults():
    """Test default configuration values."""
    config = Config()
    
    assert config.ollama_host == "http://localhost:11434"
    assert config.ollama_model == "llama2"
    assert config.agent_name == "VictorUno"
    assert config.web_host == "0.0.0.0"
    assert config.web_port == 8000
    assert config.gui_theme == "dark"
    assert config.chrome_headless is True


def test_config_from_env():
    """Test configuration from environment variables."""
    # Set environment variables
    os.environ["OLLAMA_HOST"] = "http://test:11434"
    os.environ["OLLAMA_MODEL"] = "test-model"
    os.environ["AGENT_NAME"] = "TestAgent"
    os.environ["WEB_PORT"] = "9000"
    
    try:
        config = Config.from_env()
        
        assert config.ollama_host == "http://test:11434"
        assert config.ollama_model == "test-model"
        assert config.agent_name == "TestAgent"
        assert config.web_port == 9000
    
    finally:
        # Clean up environment variables
        for key in ["OLLAMA_HOST", "OLLAMA_MODEL", "AGENT_NAME", "WEB_PORT"]:
            if key in os.environ:
                del os.environ[key]


def test_config_directories_creation():
    """Test that configuration creates necessary directories."""
    with tempfile.TemporaryDirectory() as temp_dir:
        data_dir = Path(temp_dir) / "test_data"
        
        config = Config(data_dir=data_dir)
        
        assert config.data_dir.exists()
        assert config.documents_dir.exists()


def test_config_to_dict():
    """Test configuration serialization to dictionary."""
    config = Config()
    config_dict = config.to_dict()
    
    assert isinstance(config_dict, dict)
    assert "ollama_host" in config_dict
    assert "agent_name" in config_dict
    assert config_dict["ollama_host"] == "http://localhost:11434"