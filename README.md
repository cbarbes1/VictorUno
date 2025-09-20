# VictorUno

**Personalized Agent to Research, Develop, and Optimize**

VictorUno is a powerful AI-powered agent built with Python that provides intelligent capabilities for research, development, and optimization tasks. It leverages modern language models through LangChain and LangGraph to deliver conversational AI experiences across multiple interfaces including Python API, command-line interface, and web services.

## 🌟 Key Features

- **🔬 Research Capabilities**: AI-powered research and information gathering on any topic
- **🛠️ Development Support**: Assistance with project development and solution creation  
- **⚡ Optimization Tools**: System and process optimization recommendations
- **🌤️ Weather Integration**: Real-time weather information through OpenWeatherMap API
- **🤖 Multiple LLM Backends**: Support for both local (Ollama) and cloud (Anthropic Claude) models
- **💻 Multi-Interface**: Python package, CLI tool, and FastAPI web server
- **🐳 Docker Ready**: Full containerization support for easy deployment
- **🔧 Extensible Architecture**: Built with LangChain tools for easy customization

## 🚀 Quick Start

### Python Package Usage

```python
from victoruno import VictorUno

# Create an agent instance
agent = VictorUno(name="MyAgent")

# Research a topic
research_result = agent.research("quantum computing")
print(research_result)

# Develop a project concept
dev_result = agent.develop("mobile chat application")
print(dev_result)

# Get optimization suggestions
optimize_result = agent.optimize("database performance")
print(optimize_result)

# Check weather (requires API key)
weather_result = agent.weather("San Francisco")
print(weather_result)

# Get agent information
info = agent.get_info()
print(f"Agent: {info['name']}, Version: {info['version']}")
```

### Command Line Interface

```bash
# Get agent information
victoruno info

# Research with default local model
victoruno research "artificial intelligence trends"

# Use remote Anthropic model
victoruno --mode remote --model claude-3-sonnet-20240229 research "blockchain technology"

# Development assistance
victoruno develop "web scraping tool"

# Optimization recommendations
victoruno optimize "website loading speed"

# Weather information (requires OPENWEATHERMAP_API_KEY)
victoruno weather "New York"

# Custom agent configuration
victoruno --name "MyCustomAgent" --model llama3.1:8b info
```

### Web Server

```bash
# Start the FastAPI server
langgraph-agent

# Or with custom configuration
HOST=0.0.0.0 PORT=8080 OLLAMA_MODEL=llama3.1:8b langgraph-agent
```

## 📦 Installation

### Prerequisites

- **Python 3.11 or higher**
- **Local LLM Backend** (Ollama) OR **Remote API Access** (Anthropic Claude)
- **OpenWeatherMap API Key** (optional, for weather features)

### Standard Installation

```bash
git clone https://github.com/cbarbes1/VictorUno.git
cd VictorUno
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/cbarbes1/VictorUno.git
cd VictorUno
pip install -e .[dev]
```

### Docker Installation

```bash
# Clone the repository
git clone https://github.com/cbarbes1/VictorUno.git
cd VictorUno

# Build and run with Docker Compose
docker-compose --profile prod up --build

# For development with hot-reload
docker-compose --profile dev up --build
```

## ⚙️ Configuration

### Environment Variables

VictorUno supports configuration through environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENWEATHERMAP_API_KEY` | API key for weather functionality | None | No* |
| `ANTHROPIC_API_KEY` | API key for Anthropic Claude models | None | Yes (remote mode) |
| `OLLAMA_HOST` | Ollama server endpoint | `http://localhost:11434` | No |
| `OLLAMA_MODEL` | Default Ollama model name | `gemma3:latest` | No |
| `HOST` | Web server bind address | `0.0.0.0` | No |
| `PORT` | Web server port | `8000` | No |

*Weather functionality will be disabled without API key

### Setting Up API Keys

#### OpenWeatherMap API Key (Optional)
1. Visit [OpenWeatherMap](https://openweathermap.org/api) and create a free account
2. Generate an API key from your dashboard
3. Set the environment variable:
   ```bash
   export OPENWEATHERMAP_API_KEY="your_api_key_here"
   ```

#### Anthropic API Key (For Remote Mode)
1. Visit [Anthropic Console](https://console.anthropic.com/) and create an account
2. Generate an API key from your dashboard
3. Set the environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your_anthropic_key_here"
   ```

### Model Configuration

#### Local Models (Ollama)
VictorUno supports any Ollama model. Popular choices:

```bash
# Pull models using Ollama CLI
ollama pull llama3.1:8b
ollama pull gemma:latest
ollama pull codellama:latest
ollama pull mistral:latest

# Use in VictorUno
agent = VictorUno(mode="local", model="llama3.1:8b")
```

#### Remote Models (Anthropic Claude)
Supported Claude models:

```python
# Available models
agent = VictorUno(mode="remote", model="claude-3-sonnet-20240229")
agent = VictorUno(mode="remote", model="claude-3-opus-20240229")
agent = VictorUno(mode="remote", model="claude-3-haiku-20240307")
```

## 🏗️ Architecture

VictorUno is built with a modular architecture:

```
├── src/victoruno/
│   ├── __init__.py          # Package initialization and exports
│   ├── core.py              # Main VictorUno agent class
│   ├── cli.py               # Command-line interface
│   └── app.py               # FastAPI web application
├── src/tests/               # Test suite
├── docker-compose.yaml      # Container orchestration
├── Dockerfile              # Container configuration
└── pyproject.toml          # Modern Python packaging
```

### Core Components

1. **VictorUno Agent Class** (`core.py`)
   - Main agent logic and LLM integration
   - Supports both local and remote backends
   - Tool integration (weather API)
   - Method implementations for research, development, optimization

2. **CLI Interface** (`cli.py`)
   - Command-line argument parsing
   - Agent configuration and execution
   - User-friendly error handling

3. **Web Application** (`app.py`)
   - FastAPI-based HTTP server
   - Chat endpoint for conversational interactions
   - Health check endpoints
   - LangGraph integration ready

4. **Tool Integration**
   - OpenWeatherMap API wrapper
   - Extensible tool framework via LangChain
   - Automatic tool binding to LLM

## 📚 Detailed Usage

### Python API Reference

#### VictorUno Class

```python
class VictorUno:
    def __init__(self, name: str = "VictorUno", mode: str = "local", model: str = "gemma3:latest"):
        """
        Initialize the VictorUno agent.

        Args:
            name (str): Name of the agent instance
            mode (str): "local" for Ollama, "remote" for Anthropic
            model (str): Model identifier:
                - Local: Ollama model name (e.g., "llama3.1:8b", "gemma:latest")
                - Remote: Anthropic model name (e.g., "claude-3-sonnet-20240229")
        """
```

#### Core Methods

```python
def research(self, topic: str) -> str:
    """
    Research a given topic using AI.
    
    Args:
        topic (str): The topic to research
        
    Returns:
        str: Comprehensive research results and description
    """

def develop(self, project: str) -> str:
    """
    Get development assistance for a project.
    
    Args:
        project (str): The project to develop
        
    Returns:
        str: Development suggestions and guidance
    """

def optimize(self, target: str) -> str:
    """
    Get optimization recommendations.
    
    Args:
        target (str): The system or process to optimize
        
    Returns:
        str: Optimization strategies and recommendations
    """

def weather(self, prompt: str) -> str:
    """
    Get weather information for a location.
    
    Args:
        prompt (str): Location query
        
    Returns:
        str: Weather information (requires OPENWEATHERMAP_API_KEY)
    """

def get_info(self) -> dict:
    """
    Get information about the agent.
    
    Returns:
        dict: Agent metadata including name, version, and capabilities
    """
```

### CLI Usage Examples

```bash
# Basic commands
victoruno info
victoruno research "machine learning algorithms"
victoruno develop "REST API for user management"
victoruno optimize "PostgreSQL query performance"

# Model and configuration options
victoruno --mode local --model llama3.1:8b research "climate change"
victoruno --mode remote --model claude-3-sonnet-20240229 develop "chatbot"
victoruno --name "ResearchBot" --model codellama:latest develop "Python script"

# Weather functionality (requires API key)
victoruno weather "London weather forecast"
victoruno weather "temperature in Tokyo"
```

### Web API Usage

Start the server:
```bash
langgraph-agent
```

API Endpoints:

```bash
# Health check
curl http://localhost:8000/

# Chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '"What is quantum computing?"'
```

## 🐳 Docker Usage

### Production Deployment

```bash
# Build and start production container
docker-compose --profile prod up --build

# Run in background
docker-compose --profile prod up -d --build

# View logs
docker-compose logs -f agent
```

### Development Mode

```bash
# Start development container with hot-reload
docker-compose --profile dev up --build

# The container mounts the source code for live editing
```

### Custom Configuration

```yaml
# docker-compose.override.yml
version: "3.9"
services:
  agent:
    environment:
      OLLAMA_MODEL: llama3.1:8b
      OPENWEATHERMAP_API_KEY: your_key_here
      PORT: "9000"
    ports:
      - "9000:9000"
```

## 🧪 Development

### Development Environment Setup

1. **Clone and Install**
   ```bash
   git clone https://github.com/cbarbes1/VictorUno.git
   cd VictorUno
   pip install -e .[dev]
   ```

2. **Set Up Pre-commit Hooks** (optional)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env  # Create from template if available
   # Edit .env with your API keys
   ```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=victoruno

# Run specific test file
pytest src/tests/test_core.py

# Verbose output
pytest -v

# Note: Tests require OPENWEATHERMAP_API_KEY environment variable
export OPENWEATHERMAP_API_KEY="your_key_here"
pytest
```

### Code Quality

```bash
# Format code
black src/ tests/

# Check formatting
black --check src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/victoruno/

# Run all quality checks
black src/ tests/ && flake8 src/ tests/ && mypy src/victoruno/
```

### Project Structure

```
VictorUno/
├── src/
│   ├── victoruno/
│   │   ├── __init__.py      # Package exports
│   │   ├── core.py          # Main agent class
│   │   ├── cli.py           # CLI interface
│   │   └── app.py           # FastAPI application
│   └── tests/
│       ├── __init__.py      # Test configuration
│       └── test_core.py     # Core functionality tests
├── docker-compose.yaml      # Container orchestration
├── Dockerfile              # Container definition
├── pyproject.toml          # Python project configuration
├── requirements.txt        # Dependency list
├── setup.py               # Legacy setup (compatibility)
├── LICENSE                # MIT license
└── README.md              # This documentation
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Missing API Keys
**Error**: `ValidationError: Did not find openweathermap_api_key`
**Solution**: Set the `OPENWEATHERMAP_API_KEY` environment variable or weather functionality will be limited.

```bash
export OPENWEATHERMAP_API_KEY="your_key_here"
```

#### 2. Ollama Connection Issues
**Error**: `ConnectionError: Cannot connect to Ollama`
**Solution**: Ensure Ollama is running and accessible.

```bash
# Start Ollama
ollama serve

# Pull a model
ollama pull gemma:latest

# Test connection
curl http://localhost:11434/api/tags
```

#### 3. Anthropic API Issues
**Error**: `AuthenticationError: Invalid API key`
**Solution**: Verify your Anthropic API key is correct.

```bash
export ANTHROPIC_API_KEY="your_valid_key_here"
```

#### 4. Docker Issues
**Error**: `Cannot connect to Docker daemon`
**Solution**: Ensure Docker is running and accessible.

```bash
# Check Docker status
docker info

# Start Docker (Linux)
sudo systemctl start docker
```

#### 5. Port Already in Use
**Error**: `Address already in use: 8000`
**Solution**: Change the port or stop the conflicting service.

```bash
# Use different port
PORT=8080 langgraph-agent

# Or find what's using port 8000
lsof -i :8000
```

### Getting Help

1. **Check the logs**: Most issues will show detailed error messages
2. **Environment variables**: Verify all required environment variables are set
3. **Dependencies**: Ensure all dependencies are installed with `pip install -e .[dev]`
4. **API connectivity**: Test external API connections independently
5. **Model availability**: Verify Ollama models are pulled and available

## 🤝 Contributing

We welcome contributions to VictorUno! Here's how to get started:

### Contributing Process

1. **Fork the Repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/VictorUno.git
   cd VictorUno
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-new-feature
   ```

3. **Make Your Changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   # Run tests
   pytest

   # Check code quality
   black src/ tests/
   flake8 src/ tests/
   mypy src/victoruno/
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add amazing new feature"
   git push origin feature/amazing-new-feature
   ```

6. **Create Pull Request**
   - Go to GitHub and create a pull request
   - Provide a clear description of your changes
   - Link any related issues

### Development Guidelines

- **Code Style**: Follow PEP 8, use Black for formatting
- **Type Hints**: Add type hints for all functions
- **Documentation**: Update docstrings and README for new features
- **Tests**: Maintain test coverage above 80%
- **Commit Messages**: Use clear, descriptive commit messages

### Areas for Contribution

- 🐛 Bug fixes and error handling improvements
- ✨ New agent capabilities and tools
- 📚 Documentation improvements
- 🧪 Test coverage expansion
- 🏗️ Architecture and performance improvements
- 🔧 DevOps and deployment enhancements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/) for LLM integration
- Uses [LangGraph](https://langgraph.com/) for agent workflows
- Powered by [FastAPI](https://fastapi.tiangolo.com/) for web services
- Weather data from [OpenWeatherMap](https://openweathermap.org/)
- Local LLM support via [Ollama](https://ollama.ai/)
- Remote LLM support via [Anthropic Claude](https://anthropic.com/)

---

**Happy building with VictorUno! 🚀**

For questions, issues, or suggestions, please [open an issue](https://github.com/cbarbes1/VictorUno/issues) on GitHub.
