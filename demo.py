#!/usr/bin/env python3
"""
VictorUno Demo Script

This script demonstrates the VictorUno personal agent functionality
without requiring external dependencies like LangChain or Ollama.
"""

import asyncio
import sys
from pathlib import Path

# Add the source directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def demo_basic_chat():
    """Demonstrate basic chat functionality."""
    print("🤖 VictorUno Demo - Basic Chat")
    print("=" * 50)
    
    try:
        from victoruno.core.agent import VictorUnoAgent
        from victoruno.core.config import Config
        
        # Create configuration
        config = Config()
        print(f"Agent Name: {config.agent_name}")
        print(f"Ollama Host: {config.ollama_host}")
        print(f"Model: {config.ollama_model}")
        
        # Create agent
        agent = VictorUnoAgent(config)
        
        # Test basic chat
        print("\nTesting basic chat...")
        response = await agent.chat("Hello, how are you?")
        print(f"Agent: {response}")
        
        # Test follow-up
        response = await agent.chat("What can you help me with?")
        print(f"Agent: {response}")
        
        print("\n✅ Basic chat demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in basic chat demo: {e}")
        import traceback
        traceback.print_exc()

async def demo_document_processing():
    """Demonstrate document processing functionality."""
    print("\n🤖 VictorUno Demo - Document Processing")
    print("=" * 50)
    
    try:
        from victoruno.integrations.documents import DocumentProcessor
        from victoruno.core.config import Config
        
        # Create processor
        processor = DocumentProcessor(Config())
        
        # Create a sample text file
        sample_file = Path("/tmp/sample.txt")
        with open(sample_file, "w") as f:
            f.write("This is a sample document for VictorUno.\n")
            f.write("It contains multiple lines of text.\n")
            f.write("VictorUno can process various document formats.\n")
        
        # Process the document
        print(f"Processing document: {sample_file}")
        result = await processor.process_document(sample_file)
        
        if result["success"]:
            print(f"✅ Document processed successfully!")
            print(f"   Filename: {result['filename']}")
            print(f"   Word count: {result['word_count']}")
            print(f"   Character count: {result['char_count']}")
            print(f"   Content preview: {result['content'][:100]}...")
        else:
            print(f"❌ Document processing failed: {result['message']}")
        
        # Test keyword extraction
        keywords = await processor.extract_keywords(result['content'])
        print(f"   Keywords: {keywords}")
        
        # Clean up
        sample_file.unlink()
        
        print("\n✅ Document processing demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in document processing demo: {e}")
        import traceback
        traceback.print_exc()

async def demo_web_integration():
    """Demonstrate web integration functionality."""
    print("\n🤖 VictorUno Demo - Web Integration")
    print("=" * 50)
    
    try:
        from victoruno.integrations.chrome import ChromeIntegration
        from victoruno.core.config import Config
        
        # Create integration
        chrome = ChromeIntegration(Config())
        
        # Test web search (will show mock results since browsers aren't available)
        print("Testing web search...")
        results = await chrome.search_web("Python programming", num_results=3)
        
        print(f"Search results ({len(results)} found):")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['title']}")
            print(f"     URL: {result['url']}")
            print(f"     Description: {result['description'][:100]}...")
            print()
        
        print("✅ Web integration demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in web integration demo: {e}")
        import traceback
        traceback.print_exc()

def demo_configuration():
    """Demonstrate configuration functionality."""
    print("\n🤖 VictorUno Demo - Configuration")
    print("=" * 50)
    
    try:
        from victoruno.core.config import Config
        
        # Test default configuration
        config = Config()
        print("Default configuration:")
        config_dict = config.to_dict()
        for key, value in config_dict.items():
            print(f"  {key}: {value}")
        
        # Test directories creation
        print(f"\nData directory: {config.data_dir}")
        print(f"Documents directory: {config.documents_dir}")
        print(f"Data directory exists: {config.data_dir.exists()}")
        print(f"Documents directory exists: {config.documents_dir.exists()}")
        
        print("\n✅ Configuration demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in configuration demo: {e}")
        import traceback
        traceback.print_exc()

def demo_utilities():
    """Demonstrate utility functions."""
    print("\n🤖 VictorUno Demo - Utilities")
    print("=" * 50)
    
    try:
        from victoruno.utils import (
            truncate_text, format_file_size, clean_filename,
            validate_url, extract_domain
        )
        
        # Test text truncation
        long_text = "This is a very long text that should be truncated for display purposes."
        truncated = truncate_text(long_text, max_length=30)
        print(f"Original: {long_text}")
        print(f"Truncated: {truncated}")
        
        # Test file size formatting
        sizes = [1024, 1024*1024, 1024*1024*1024]
        for size in sizes:
            formatted = format_file_size(size)
            print(f"Size {size} bytes: {formatted}")
        
        # Test filename cleaning
        dirty_filename = "bad<>filename:with|invalid*chars.txt"
        clean = clean_filename(dirty_filename)
        print(f"Original filename: {dirty_filename}")
        print(f"Clean filename: {clean}")
        
        # Test URL validation
        urls = ["https://github.com", "not-a-url", "http://localhost:8000"]
        for url in urls:
            valid = validate_url(url)
            domain = extract_domain(url)
            print(f"URL: {url} - Valid: {valid}, Domain: {domain}")
        
        print("\n✅ Utilities demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in utilities demo: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Run all demos."""
    print("🚀 VictorUno Personal Agent Demo")
    print("=" * 60)
    print("This demo showcases VictorUno's capabilities without requiring")
    print("external dependencies like LangChain, Ollama, or Chrome.")
    print("=" * 60)
    
    # Run all demos
    demo_configuration()
    demo_utilities()
    await demo_document_processing()
    await demo_web_integration()
    await demo_basic_chat()
    
    print("\n🎉 All demos completed!")
    print("\nTo use VictorUno with full functionality:")
    print("1. Install dependencies: pip install -e .")
    print("2. Install and start Ollama: ollama serve")
    print("3. Pull a model: ollama pull llama2")
    print("4. Run VictorUno: victoruno")
    print("\nFor web interface: victoruno --web")
    print("For GUI interface: victoruno --gui")

if __name__ == "__main__":
    asyncio.run(main())