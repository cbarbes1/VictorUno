#!/usr/bin/env python3
"""
FastAPI Web Server Examples

This script demonstrates how to interact with the VictorUno
FastAPI web server programmatically.
"""

import asyncio
import aiohttp
import json
import time


async def test_health_endpoint():
    """Test the health check endpoint."""
    print("🏥 Testing Health Endpoint")
    print("-" * 30)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8000/') as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Health check: {data}")
                else:
                    print(f"   ❌ Health check failed: {response.status}")
    except Exception as e:
        print(f"   ❌ Could not connect to server: {e}")
        print("   💡 Make sure to start the server first: langgraph-agent")


async def test_chat_endpoint():
    """Test the chat endpoint with various queries."""
    print("\n💬 Testing Chat Endpoint")
    print("-" * 30)
    
    test_messages = [
        "What is machine learning?",
        "How do I optimize database performance?",
        "Create a simple Python function to calculate fibonacci numbers",
        "What are the latest trends in web development?"
    ]
    
    try:
        async with aiohttp.ClientSession() as session:
            for message in test_messages:
                print(f"\n📤 Sending: {message[:50]}...")
                
                async with session.post(
                    'http://localhost:8000/chat',
                    json=message,
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        reply = data.get('reply', 'No reply')
                        print(f"   📥 Response: {reply[:100]}...")
                    else:
                        print(f"   ❌ Error: {response.status}")
                
                # Small delay between requests
                await asyncio.sleep(1)
                
    except Exception as e:
        print(f"   ❌ Could not test chat endpoint: {e}")


def show_curl_examples():
    """Show curl command examples for API testing."""
    print("\n🔧 Curl Command Examples")
    print("-" * 30)
    
    examples = [
        {
            "description": "Health check",
            "command": "curl http://localhost:8000/"
        },
        {
            "description": "Simple chat query",
            "command": '''curl -X POST http://localhost:8000/chat \\
  -H "Content-Type: application/json" \\
  -d '"What is artificial intelligence?"' '''
        },
        {
            "description": "Development assistance",
            "command": '''curl -X POST http://localhost:8000/chat \\
  -H "Content-Type: application/json" \\
  -d '"Help me create a REST API for user management"' '''
        },
        {
            "description": "Optimization query",
            "command": '''curl -X POST http://localhost:8000/chat \\
  -H "Content-Type: application/json" \\
  -d '"How can I optimize my React application performance?"' '''
        }
    ]
    
    for example in examples:
        print(f"\n{example['description']}:")
        print(f"   {example['command']}")


def show_python_requests_examples():
    """Show Python requests library examples."""
    print("\n🐍 Python Requests Examples")
    print("-" * 35)
    
    print("""
import requests
import json

# Health check
response = requests.get('http://localhost:8000/')
print(f"Health: {response.json()}")

# Chat interaction
chat_data = "Explain quantum computing in simple terms"
response = requests.post(
    'http://localhost:8000/chat',
    json=chat_data,
    headers={'Content-Type': 'application/json'}
)

if response.status_code == 200:
    result = response.json()
    print(f"Reply: {result['reply']}")
else:
    print(f"Error: {response.status_code}")

# Batch processing multiple queries
queries = [
    "What is Docker?",
    "How do I use Git effectively?", 
    "Explain microservices architecture"
]

results = []
for query in queries:
    response = requests.post(
        'http://localhost:8000/chat',
        json=query,
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code == 200:
        results.append({
            'query': query,
            'reply': response.json()['reply']
        })

# Save results
with open('api_results.json', 'w') as f:
    json.dump(results, f, indent=2)
""")


def show_javascript_examples():
    """Show JavaScript fetch API examples."""
    print("\n🌐 JavaScript Fetch Examples")
    print("-" * 35)
    
    print("""
// Health check
fetch('http://localhost:8000/')
  .then(response => response.json())
  .then(data => console.log('Health:', data))
  .catch(error => console.error('Error:', error));

// Chat interaction
async function askVictorUno(message) {
  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(message)
    });
    
    if (response.ok) {
      const data = await response.json();
      return data.reply;
    } else {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}

// Usage
askVictorUno("How do I deploy a Node.js application?")
  .then(reply => console.log('VictorUno says:', reply));

// Multiple queries
const queries = [
  "What is TypeScript?",
  "How do I handle errors in JavaScript?",
  "Explain async/await"
];

Promise.all(queries.map(q => askVictorUno(q)))
  .then(replies => {
    queries.forEach((q, i) => {
      console.log(`Q: ${q}`);
      console.log(`A: ${replies[i]}`);
      console.log('---');
    });
  });
""")


def show_server_configuration():
    """Show server configuration options."""
    print("\n⚙️  Server Configuration")
    print("-" * 30)
    
    print("Environment variables for server configuration:")
    print("   HOST=0.0.0.0          # Bind address")
    print("   PORT=8000             # Server port")
    print("   OLLAMA_MODEL=llama3.1:8b  # Default model")
    print("   OLLAMA_HOST=http://localhost:11434  # Ollama endpoint")
    
    print("\nStarting server with custom configuration:")
    print("   HOST=127.0.0.1 PORT=9000 langgraph-agent")
    
    print("\nDocker deployment:")
    print("   docker-compose --profile prod up")
    print("   # or for development:")
    print("   docker-compose --profile dev up")


async def main():
    """Run all web API examples."""
    print("🌐 VictorUno FastAPI Web Server Examples")
    print("=" * 55)
    
    await test_health_endpoint()
    await test_chat_endpoint()
    
    show_curl_examples()
    show_python_requests_examples()
    show_javascript_examples()
    show_server_configuration()
    
    print("\n✅ Web API examples completed!")
    print("\n💡 To test these examples:")
    print("   1. Start the server: langgraph-agent")
    print("   2. Run this script: python examples/web_api_examples.py")
    print("   3. Or copy the curl/code examples above")


if __name__ == "__main__":
    asyncio.run(main())