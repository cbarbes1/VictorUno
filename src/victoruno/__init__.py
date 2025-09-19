"""
VictorUno - Personalized Agent to Research, Develop, and Optimize

A personal agent system using LangChain and LangGraph with local Ollama models.
"""

__version__ = "0.1.0"
__author__ = "Cole Barbes"

from .core.agent import VictorUnoAgent
from .core.config import Config

__all__ = ["VictorUnoAgent", "Config"]