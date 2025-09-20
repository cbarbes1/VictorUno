#!/usr/bin/env python3
"""
CLI Usage Examples for VictorUno

This script demonstrates various CLI usage patterns.
Run this to see example CLI commands without executing them.
"""

def show_basic_cli_examples():
    """Show basic CLI command examples."""
    print("📋 Basic CLI Commands")
    print("-" * 30)
    
    commands = [
        ("Get agent information", "victoruno info"),
        ("Research a topic", 'victoruno research "artificial intelligence"'),
        ("Development help", 'victoruno develop "web scraping tool"'),
        ("Optimization advice", 'victoruno optimize "database performance"'),
        ("Weather information", 'victoruno weather "New York weather"'),
    ]
    
    for description, command in commands:
        print(f"\n{description}:")
        print(f"   $ {command}")


def show_advanced_cli_examples():
    """Show advanced CLI configuration examples."""
    print("\n⚙️  Advanced CLI Configuration")
    print("-" * 40)
    
    examples = [
        ("Custom agent name", 'victoruno --name "MyResearchBot" info'),
        ("Use specific local model", 'victoruno --model llama3.1:8b research "quantum physics"'),
        ("Use remote Anthropic model", 'victoruno --mode remote --model claude-3-sonnet-20240229 develop "chatbot"'),
        ("Full custom configuration", 'victoruno --name "SpecialAgent" --mode local --model codellama:latest develop "Python script"'),
    ]
    
    for description, command in examples:
        print(f"\n{description}:")
        print(f"   $ {command}")


def show_environment_examples():
    """Show how to use environment variables with CLI."""
    print("\n🌍 Environment Variable Usage")
    print("-" * 40)
    
    examples = [
        ("Set API key and run", 'OPENWEATHERMAP_API_KEY="your_key" victoruno weather "Tokyo"'),
        ("Use Anthropic with API key", 'ANTHROPIC_API_KEY="your_key" victoruno --mode remote research "AI trends"'),
        ("Custom Ollama host", 'OLLAMA_HOST="http://192.168.1.100:11434" victoruno research "blockchain"'),
        ("Multiple environment vars", 'OPENWEATHERMAP_API_KEY="key1" ANTHROPIC_API_KEY="key2" victoruno info'),
    ]
    
    for description, command in examples:
        print(f"\n{description}:")
        print(f"   $ {command}")


def show_error_handling_examples():
    """Show common error scenarios and solutions."""
    print("\n🚨 Common Error Scenarios & Solutions")
    print("-" * 45)
    
    scenarios = [
        {
            "error": "Missing target argument",
            "command": "victoruno research",
            "solution": 'victoruno research "your topic here"'
        },
        {
            "error": "OpenWeatherMap API key not found",
            "command": "victoruno weather London",
            "solution": 'OPENWEATHERMAP_API_KEY="your_key" victoruno weather London'
        },
        {
            "error": "Ollama connection refused",
            "command": "victoruno research AI",
            "solution": "Start Ollama: ollama serve, then try again"
        },
        {
            "error": "Anthropic API authentication",
            "command": "victoruno --mode remote research AI",
            "solution": 'ANTHROPIC_API_KEY="your_key" victoruno --mode remote research AI'
        }
    ]
    
    for scenario in scenarios:
        print(f"\n❌ {scenario['error']}:")
        print(f"   Command: {scenario['command']}")
        print(f"   Solution: {scenario['solution']}")


def show_batch_processing_examples():
    """Show how to use CLI in batch processing scenarios."""
    print("\n📦 Batch Processing Examples")
    print("-" * 35)
    
    print("\nBash script for multiple research topics:")
    print("""   #!/bin/bash
   topics=("AI" "blockchain" "quantum computing" "renewable energy")
   for topic in "${topics[@]}"; do
       echo "Researching: $topic"
       victoruno research "$topic" > "research_$topic.txt"
   done""")
    
    print("\nPython script using subprocess:")
    print("""   import subprocess
   import json
   
   topics = ["machine learning", "data science", "web development"]
   results = {}
   
   for topic in topics:
       result = subprocess.run(
           ["victoruno", "research", topic], 
           capture_output=True, text=True
       )
       results[topic] = result.stdout
   
   with open("research_results.json", "w") as f:
       json.dump(results, f, indent=2)""")


def main():
    print("🎯 VictorUno CLI Usage Examples")
    print("=" * 50)
    
    show_basic_cli_examples()
    show_advanced_cli_examples() 
    show_environment_examples()
    show_error_handling_examples()
    show_batch_processing_examples()
    
    print("\n✅ CLI examples completed!")
    print("\n💡 To actually run these commands:")
    print("   1. Ensure VictorUno is installed: pip install -e .")
    print("   2. Set up environment variables as needed")
    print("   3. Copy and paste commands into your terminal")


if __name__ == "__main__":
    main()