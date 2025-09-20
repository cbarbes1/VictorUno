#!/usr/bin/env python3
"""
Basic VictorUno Usage Examples

This script demonstrates basic usage of the VictorUno agent
for research, development, and optimization tasks.
"""

import os
from victoruno import VictorUno


def main():
    print("🤖 VictorUno Basic Usage Examples")
    print("=" * 50)
    
    # Create agent instance
    print("\n1. Creating VictorUno agent...")
    agent = VictorUno(name="ExampleAgent")
    
    # Get agent info
    print("\n2. Agent Information:")
    info = agent.get_info()
    print(f"   Name: {info['name']}")
    print(f"   Version: {info['version']}")
    print(f"   Capabilities: {', '.join(info['capabilities'])}")
    
    # Development assistance
    print("\n3. Development Assistance:")
    dev_result = agent.develop("REST API for a todo application")
    print(f"   {dev_result}")
    
    # Optimization suggestions
    print("\n4. Optimization Suggestions:")
    opt_result = agent.optimize("React application performance")
    print(f"   {opt_result}")
    
    # Weather (if API key is available)
    print("\n5. Weather Information:")
    if os.getenv("OPENWEATHERMAP_API_KEY"):
        try:
            weather_result = agent.weather("San Francisco")
            print(f"   {weather_result}")
        except Exception as e:
            print(f"   Weather error: {e}")
    else:
        print("   ⚠️  Set OPENWEATHERMAP_API_KEY to test weather functionality")
    
    # Research (requires Ollama or Anthropic)
    print("\n6. Research Capability:")
    try:
        research_result = agent.research("machine learning trends 2024")
        print(f"   {research_result}")
    except Exception as e:
        print(f"   ⚠️  Research requires Ollama (local) or Anthropic API key (remote)")
        print(f"   Error: {e}")
    
    print("\n✅ Examples completed!")


if __name__ == "__main__":
    main()