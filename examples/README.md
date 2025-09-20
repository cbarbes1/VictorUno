# VictorUno Examples

This directory contains comprehensive examples demonstrating various ways to use VictorUno.

## 📁 Example Files

### 🟢 Basic Examples
- **`basic_usage.py`** - Simple examples showing core functionality
- **`cli_examples.py`** - Command-line interface usage patterns

### 🔵 Advanced Examples  
- **`advanced_usage.py`** - Advanced configuration and model selection
- **`web_api_examples.py`** - FastAPI web server integration examples

## 🚀 Running the Examples

### Prerequisites

1. **Install VictorUno:**
   ```bash
   cd VictorUno
   pip install -e .[dev]
   ```

2. **Set up environment variables (copy from .env.example):**
   ```bash
   export OPENWEATHERMAP_API_KEY="your_key_here"
   export ANTHROPIC_API_KEY="your_key_here"  # For remote mode
   ```

3. **For local mode, ensure Ollama is running:**
   ```bash
   ollama serve
   ollama pull gemma3:latest  # or your preferred model
   ```

### Running Individual Examples

```bash
# Basic usage examples
python examples/basic_usage.py

# CLI examples (shows commands, doesn't run them)
python examples/cli_examples.py

# Advanced configuration examples
python examples/advanced_usage.py

# Web API examples (requires server to be running)
# Terminal 1: Start server
langgraph-agent

# Terminal 2: Run examples
python examples/web_api_examples.py
```

## 📋 Example Categories

### 1. Basic Usage (`basic_usage.py`)
- Creating agent instances
- Using core methods (research, develop, optimize)
- Weather functionality
- Error handling

### 2. CLI Examples (`cli_examples.py`)
Shows command patterns for:
- Basic commands (`victoruno info`, `victoruno research`)
- Configuration options (`--mode`, `--model`, `--name`)
- Environment variables
- Error scenarios and solutions
- Batch processing

### 3. Advanced Usage (`advanced_usage.py`)
Demonstrates:
- Different local models (Ollama)
- Remote models (Anthropic Claude)
- Custom agent configurations
- Environment variable effects

### 4. Web API Examples (`web_api_examples.py`)
Covers:
- Health check endpoints
- Chat API interactions
- Python requests usage
- JavaScript fetch examples
- curl command examples
- Server configuration

## 🎯 Quick Start Examples

### Python Package
```python
from victoruno import VictorUno

# Create agent
agent = VictorUno(name="MyAgent")

# Use capabilities
result = agent.develop("Python web scraper")
print(result)
```

### Command Line
```bash
# Get info
victoruno info

# Research a topic
victoruno research "machine learning"

# Custom configuration
victoruno --mode local --model llama3.1:8b develop "chatbot"
```

### Web API
```bash
# Start server
langgraph-agent

# Test health
curl http://localhost:8000/

# Chat interaction
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '"Explain Docker containers"'
```

## 🔧 Configuration Examples

### Environment Variables
```bash
# For weather functionality
export OPENWEATHERMAP_API_KEY="your_weather_api_key"

# For remote AI models
export ANTHROPIC_API_KEY="your_anthropic_key"

# Custom Ollama configuration
export OLLAMA_HOST="http://192.168.1.100:11434"
export OLLAMA_MODEL="llama3.1:8b"
```

### Model Selection
```python
# Local models (requires Ollama)
agent = VictorUno(mode="local", model="gemma3:latest")
agent = VictorUno(mode="local", model="llama3.1:8b")
agent = VictorUno(mode="local", model="codellama:latest")

# Remote models (requires Anthropic API key)
agent = VictorUno(mode="remote", model="claude-3-sonnet-20240229")
agent = VictorUno(mode="remote", model="claude-3-haiku-20240307")
```

## ⚠️ Troubleshooting Examples

### Common Issues and Solutions

1. **Missing API Keys:**
   ```bash
   # Error: OpenWeatherMap API key not found
   export OPENWEATHERMAP_API_KEY="your_key"
   
   # Error: Anthropic API authentication failed
   export ANTHROPIC_API_KEY="your_key"
   ```

2. **Ollama Connection Issues:**
   ```bash
   # Start Ollama service
   ollama serve
   
   # Pull required models
   ollama pull gemma3:latest
   
   # Check Ollama status
   curl http://localhost:11434/api/tags
   ```

3. **Port Conflicts:**
   ```bash
   # Use different port for web server
   PORT=8080 langgraph-agent
   
   # Check what's using port 8000
   lsof -i :8000
   ```

## 🔄 Interactive Examples

### Jupyter Notebook Usage
```python
# In Jupyter notebook
%load_ext autoreload
%autoreload 2

from victoruno import VictorUno
agent = VictorUno()

# Interactive development
topics = ["AI", "blockchain", "quantum computing"]
for topic in topics:
    result = agent.research(topic)
    print(f"Research on {topic}:")
    print(result)
    print("-" * 50)
```

### REPL Usage
```python
# In Python REPL
>>> from victoruno import VictorUno
>>> agent = VictorUno(name="InteractiveAgent")
>>> agent.get_info()
{'name': 'InteractiveAgent', 'version': '0.1.0', 'capabilities': ['research', 'develop', 'optimize']}
>>> result = agent.optimize("code performance")
>>> print(result)
```

## 📝 Example Output

### Research Example
```
Researching topic: machine learning
Description: Machine learning is a subset of artificial intelligence that enables 
computers to learn and improve from experience without being explicitly programmed.
It involves algorithms that can identify patterns in data and make predictions or 
decisions based on that analysis.
```

### Development Example
```
Developing project: REST API for user management

Here's a comprehensive approach to developing a REST API for user management:
- Design database schema for users
- Set up authentication and authorization
- Implement CRUD operations (Create, Read, Update, Delete)
- Add input validation and error handling
- Include API documentation with OpenAPI/Swagger
```

## 🎉 Next Steps

After trying these examples:

1. **Explore the main README.md** for complete documentation
2. **Check out the test suite** in `src/tests/` for more usage patterns
3. **Contribute your own examples** via pull requests
4. **Join the community** and share your VictorUno projects

## 🤝 Contributing Examples

We welcome new examples! Please:

1. Follow the existing code style
2. Include clear documentation
3. Add error handling
4. Test with different configurations
5. Submit a pull request

Happy coding with VictorUno! 🚀