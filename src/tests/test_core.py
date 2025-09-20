"""
Tests for VictorUno core functionality.
"""

import pytest
from victoruno.core import VictorUno


class TestVictorUno:
    """Test cases for VictorUno class."""
    
    def test_initialization(self):
        """Test VictorUno initialization."""
        agent = VictorUno()
        assert agent.name == "VictorUno"
        assert agent.version == "0.1.0"
        
        custom_agent = VictorUno(name="CustomAgent")
        assert custom_agent.name == "CustomAgent"
        assert custom_agent.version == "0.1.0"
    
    def test_research(self):
        """Test research functionality."""
        agent = VictorUno()
        result = agent.research("AI")
        assert result == "Researching topic: AI"
        assert isinstance(result, str)
    
    def test_develop(self):
        """Test develop functionality."""
        agent = VictorUno()
        result = agent.develop("Web App")
        assert result == "Developing project: Web App"
        assert isinstance(result, str)
    
    def test_optimize(self):
        """Test optimize functionality."""
        agent = VictorUno()
        result = agent.optimize("Database")
        assert result == "Optimizing target: Database"
        assert isinstance(result, str)
    
    def test_get_info(self):
        """Test get_info functionality."""
        agent = VictorUno(name="TestAgent")
        info = agent.get_info()
        
        assert isinstance(info, dict)
        assert info["name"] == "TestAgent"
        assert info["version"] == "0.1.0"
        assert info["capabilities"] == ["research", "develop", "optimize"]