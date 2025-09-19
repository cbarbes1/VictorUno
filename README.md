# VictorUno
Personalized Agent to Research, Develop, and Optimize

A comprehensive personal AI assistant built with LangChain and LangGraph that interfaces with local Ollama models. VictorUno provides multiple interfaces for interaction and integrates with various tools for enhanced productivity.

## Features

### 🤖 Core Agent
- **LangChain & LangGraph Integration**: Advanced AI agent workflow using state-of-the-art frameworks
- **Local Ollama Support**: Privacy-focused with local LLM models
- **Conversation Memory**: Maintains context across interactions
- **Multi-modal Processing**: Handles text, documents, and web content

### 💻 Multiple Interfaces
- **Command Line Interface (CLI)**: Simple terminal-based interaction
- **Web Interface**: Modern web-based chat with file upload
- **GUI Application**: Native desktop application with dark/light themes
- **API Endpoints**: RESTful API for integration with other tools

### 📄 Document Processing
- **PDF Support**: Extract text from PDF documents
- **Word Documents**: Process .docx files
- **Text Files**: Support for .txt, .md, and other text formats
- **HTML Processing**: Clean text extraction from HTML files
- **Batch Processing**: Handle multiple documents simultaneously

### 🌐 Web Integration
- **Chrome Automation**: Automated web research and browsing
- **Google Search**: Integrated web search capabilities
- **Web Scraping**: Extract content from web pages
- **URL Processing**: Handle and process web links

## Installation

### Prerequisites
- Python 3.8 or higher
- Ollama installed and running locally
- Chrome browser (for web integration features)

### Install VictorUno

```bash
# Clone the repository
git clone https://github.com/cbarbes1/VictorUno.git
cd VictorUno

# Install the package
pip install -e .

# Or install with optional dependencies
pip install -e .[gui,dev]
```

### Set up Ollama
```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (e.g., llama2)
ollama pull llama2

# Start Ollama server
ollama serve
```

### Configuration
```bash
# Copy the example configuration
cp .env.example .env

# Edit the configuration file
nano .env
```

## Usage

### Command Line Interface
```bash
# Interactive chat
victoruno

# Single query
victoruno --query "What is artificial intelligence?"

# Process a document
victoruno --document path/to/document.pdf

# Start web interface
victoruno --web

# Start GUI
victoruno --gui
```

### Web Interface
```bash
# Start the web server
victoruno-web

# Or using the CLI
victoruno --web
```
Then open http://localhost:8000 in your browser.

### GUI Application
```bash
# Start the GUI
victoruno-gui

# Or using the CLI
victoruno --gui
```

### Python API
```python
import asyncio
from victoruno import VictorUnoAgent, Config

# Initialize the agent
config = Config.from_env()
agent = VictorUnoAgent(config)

# Chat with the agent
async def main():
    response = await agent.chat("Hello, how can you help me?")
    print(response)
    
    # Process a document
    result = await agent.process_document(Path("document.pdf"))
    print(result)
    
    # Perform web search
    search_results = await agent.web_search("Python programming")
    print(search_results)

asyncio.run(main())
```

## Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama2` | Default Ollama model |
| `AGENT_NAME` | `VictorUno` | Name of the agent |
| `WEB_HOST` | `0.0.0.0` | Web interface host |
| `WEB_PORT` | `8000` | Web interface port |
| `GUI_THEME` | `dark` | GUI theme (dark/light) |
| `CHROME_HEADLESS` | `true` | Run Chrome in headless mode |

## Dependencies

### Core Dependencies
- `langchain` - LLM framework
- `langgraph` - Agent workflow framework
- `ollama` - Local LLM integration
- `fastapi` - Web framework
- `pydantic` - Data validation

### Optional Dependencies
- `PyQt6` - For enhanced GUI (install with `pip install victoruno[gui]`)
- `selenium` - For Chrome automation
- `playwright` - Alternative browser automation
- `PyPDF2` - PDF processing
- `python-docx` - Word document processing
- `beautifulsoup4` - HTML processing

## Development

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Code formatting
black src/
isort src/

# Type checking
mypy src/
```

## Examples

### Document Analysis
```bash
# Upload and analyze a research paper
victoruno --document research_paper.pdf --query "Summarize the key findings"
```

### Web Research
```bash
# Research a topic using web search
victoruno --query "search for latest AI developments"
```

### Multi-modal Interaction
```python
# Process multiple documents and perform web research
agent = VictorUnoAgent()

# Process documents
await agent.process_document(Path("paper1.pdf"))
await agent.process_document(Path("paper2.pdf"))

# Ask questions about the documents
response = await agent.chat("Compare the methodologies in these papers")

# Supplement with web research
web_results = await agent.web_search("recent advances in the methodology")
```

## Architecture

VictorUno is built with a modular architecture:

```
victoruno/
├── core/           # Core agent logic and configuration
├── gui/            # Desktop GUI interface
├── web/            # Web interface and API
├── integrations/   # External service integrations
└── utils/          # Utility functions and helpers
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) for the LLM framework
- [LangGraph](https://github.com/langchain-ai/langgraph) for agent workflows
- [Ollama](https://ollama.ai/) for local LLM hosting
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
