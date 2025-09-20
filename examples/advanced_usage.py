#!/usr/bin/env python3
"""
Advanced VictorUno Configuration Examples

This script demonstrates advanced configuration options
including different models and modes.
"""

import os
from victoruno import VictorUno


def example_local_models():
    """Demonstrate using different local Ollama models."""
    print("\n🏠 Local Model Examples (Ollama)")
    print("-" * 40)
    
    models_to_try = [
        "gemma3:latest",
        "llama3.1:8b", 
        "codellama:latest",
        "mistral:latest"
    ]
    
    for model in models_to_try:
        try:
            print(f"\n📦 Testing model: {model}")
            agent = VictorUno(
                name=f"Agent-{model.replace(':', '-')}",
                mode="local",
                model=model
            )
            
            result = agent.develop("simple calculator app")
            print(f"   ✅ {model}: {result}")
            
        except Exception as e:
            print(f"   ❌ {model}: Not available ({str(e)[:50]}...)")


def example_remote_models():
    """Demonstrate using Anthropic Claude models."""
    print("\n☁️  Remote Model Examples (Anthropic)")
    print("-" * 40)
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("   ⚠️  Set ANTHROPIC_API_KEY to test remote models")
        return
    
    claude_models = [
        "claude-3-sonnet-20240229",
        "claude-3-opus-20240229", 
        "claude-3-haiku-20240307"
    ]
    
    for model in claude_models:
        try:
            print(f"\n🧠 Testing model: {model}")
            agent = VictorUno(
                name=f"Claude-Agent",
                mode="remote",
                model=model
            )
            
            result = agent.optimize("database query performance")
            print(f"   ✅ {model}: {result}")
            
        except Exception as e:
            print(f"   ❌ {model}: Error ({str(e)[:50]}...)")


def example_custom_agent():
    """Demonstrate creating a specialized agent."""
    print("\n🎯 Custom Agent Example")
    print("-" * 30)
    
    try:
        # Create a specialized research agent
        research_agent = VictorUno(
            name="ResearchBot-Pro",
            mode="local",  # or "remote" if you have Anthropic API key
            model="gemma3:latest"  # or Claude model for remote
        )
        
        print(f"Agent Info: {research_agent.get_info()}")
        
        # Multiple related research tasks
        topics = [
            "quantum computing applications",
            "sustainable energy technologies", 
            "artificial intelligence ethics"
        ]
        
        for topic in topics:
            try:
                result = research_agent.research(topic)
                print(f"\n📚 Research on '{topic}':")
                print(f"   {result[:100]}...")  # Truncate for display
            except Exception as e:
                print(f"   ❌ Could not research '{topic}': {e}")
                
    except Exception as e:
        print(f"   ❌ Could not create custom agent: {e}")


def example_environment_configuration():
    """Show how environment variables affect behavior."""
    print("\n🔧 Environment Configuration")
    print("-" * 35)
    
    env_vars = [
        "OPENWEATHERMAP_API_KEY",
        "ANTHROPIC_API_KEY", 
        "OLLAMA_HOST",
        "OLLAMA_MODEL"
    ]
    
    print("Current environment configuration:")
    for var in env_vars:
        value = os.getenv(var, "Not set")
        # Mask API keys for security
        if "API_KEY" in var and value != "Not set":
            value = f"{value[:8]}...{value[-4:]}"
        print(f"   {var}: {value}")


def main():
    print("🚀 VictorUno Advanced Configuration Examples")
    print("=" * 60)
    
    example_environment_configuration()
    example_local_models()
    example_remote_models()
    example_custom_agent()
    
    print("\n✅ Advanced examples completed!")
    print("\n💡 Tips:")
    print("   - Install Ollama and pull models for local testing")
    print("   - Get Anthropic API key for remote model access")
    print("   - Set OPENWEATHERMAP_API_KEY for weather features")


if __name__ == "__main__":
    main()