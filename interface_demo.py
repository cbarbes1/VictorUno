#!/usr/bin/env python3
"""
Simple web interface demo without heavy dependencies.
This shows the web interface structure even without FastAPI.
"""

import sys
from pathlib import Path

# Add source to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def demo_web_interface():
    """Demonstrate the web interface structure."""
    print("🌐 VictorUno Web Interface Demo")
    print("=" * 50)
    
    try:
        # Show that we can import the web module
        from victoruno.web.main import app
        print("✅ Web module imported successfully")
        
        # Show available endpoints (without running FastAPI)
        print("\nAvailable endpoints:")
        print("  GET  /          - Main chat interface")
        print("  GET  /health    - Health check")
        print("  POST /chat      - REST chat endpoint")
        print("  POST /upload    - File upload")
        print("  WS   /ws        - WebSocket chat")
        
        print("\nTo run the web interface with full functionality:")
        print("1. Install dependencies: pip install fastapi uvicorn")
        print("2. Run: victoruno --web")
        print("3. Open browser to: http://localhost:8000")
        
        print("\n📝 Features include:")
        print("  - Real-time chat with WebSocket")
        print("  - Document upload and processing")
        print("  - REST API endpoints")
        print("  - Responsive web interface")
        print("  - CORS support for integration")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def demo_cli_interface():
    """Demonstrate CLI interface."""
    print("\n💻 VictorUno CLI Interface Demo")
    print("=" * 50)
    
    try:
        from victoruno.cli import VictorUnoCLI
        print("✅ CLI module imported successfully")
        
        print("\nCLI Usage examples:")
        print("  victoruno                    # Interactive chat")
        print("  victoruno -q 'Hello'         # Single query")
        print("  victoruno -d document.pdf    # Process document")
        print("  victoruno --web              # Start web server")
        print("  victoruno --gui              # Start GUI")
        
        print("\n🔧 CLI Features:")
        print("  - Interactive chat mode")
        print("  - Single query mode")
        print("  - Document processing")
        print("  - Multiple interface launchers")
        print("  - Configuration support")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def demo_gui_interface():
    """Demonstrate GUI interface."""
    print("\n🖥️  VictorUno GUI Interface Demo")
    print("=" * 50)
    
    try:
        from victoruno.gui.main import VictorUnoGUI
        print("✅ GUI module imported successfully")
        
        print("\n🎨 GUI Features:")
        print("  - Native desktop application")
        print("  - Dark/light theme support")
        print("  - Real-time chat interface")
        print("  - Document drag-and-drop")
        print("  - Settings panel")
        print("  - Web research integration")
        print("  - Conversation management")
        
        print("\nTo run the GUI:")
        print("  victoruno --gui")
        print("  # or")
        print("  victoruno-gui")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all interface demos."""
    print("🚀 VictorUno Interface Showcase")
    print("=" * 60)
    
    demos = [
        demo_cli_interface,
        demo_web_interface,
        demo_gui_interface,
    ]
    
    success_count = 0
    for demo in demos:
        try:
            if demo():
                success_count += 1
        except Exception as e:
            print(f"❌ Demo failed: {e}")
    
    print(f"\n📊 Results: {success_count}/{len(demos)} interface demos successful")
    
    if success_count == len(demos):
        print("\n🎉 All interfaces are properly structured and ready!")
        print("\nNext steps for full deployment:")
        print("1. Install full dependencies: pip install -e .")
        print("2. Set up Ollama: ollama serve")
        print("3. Configure environment: cp .env.example .env")
        print("4. Choose your interface:")
        print("   - CLI: victoruno")
        print("   - Web: victoruno --web") 
        print("   - GUI: victoruno --gui")
    else:
        print("\n⚠️  Some interfaces had issues. Check the errors above.")

if __name__ == "__main__":
    main()