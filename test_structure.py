#!/usr/bin/env python3
"""
Simple test script to validate VictorUno structure without external dependencies.
"""

import sys
import os
from pathlib import Path

# Add the source directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that core modules can be imported."""
    print("Testing imports...")
    
    try:
        from victoruno.core.config import Config
        print("✓ Config import successful")
    except ImportError as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    try:
        # Test basic config creation
        config = Config()
        print("✓ Config instantiation successful")
        print(f"  - Agent name: {config.agent_name}")
        print(f"  - Ollama host: {config.ollama_host}")
        print(f"  - Web port: {config.web_port}")
    except Exception as e:
        print(f"✗ Config creation failed: {e}")
        return False
    
    # Test utilities
    try:
        from victoruno.utils import truncate_text, format_file_size
        print("✓ Utils import successful")
        
        # Test utility functions
        text = truncate_text("This is a long text that should be truncated", max_length=20)
        size = format_file_size(1024)
        print(f"  - Truncated text: {text}")
        print(f"  - Formatted size: {size}")
    except ImportError as e:
        print(f"✗ Utils import failed: {e}")
        return False
    
    return True

def test_directory_structure():
    """Test that all required directories exist."""
    print("\nTesting directory structure...")
    
    src_dir = Path(__file__).parent / "src" / "victoruno"
    required_dirs = ["core", "web", "gui", "integrations", "utils"]
    
    all_exist = True
    for dir_name in required_dirs:
        dir_path = src_dir / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name} directory exists")
        else:
            print(f"✗ {dir_name} directory missing")
            all_exist = False
    
    return all_exist

def test_configuration():
    """Test configuration functionality."""
    print("\nTesting configuration...")
    
    try:
        from victoruno.core.config import Config
        
        # Test default config
        config = Config()
        config_dict = config.to_dict()
        
        required_keys = ["ollama_host", "agent_name", "web_port", "gui_theme"]
        for key in required_keys:
            if key in config_dict:
                print(f"✓ Config has {key}: {config_dict[key]}")
            else:
                print(f"✗ Config missing {key}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    root_dir = Path(__file__).parent
    required_files = [
        "pyproject.toml",
        "README.md",
        "LICENSE",
        ".env.example",
        "src/victoruno/__init__.py",
        "src/victoruno/cli.py",
        "src/victoruno/core/__init__.py",
        "src/victoruno/core/config.py",
        "src/victoruno/core/agent.py",
        "src/victoruno/web/__init__.py",
        "src/victoruno/web/main.py",
        "src/victoruno/gui/__init__.py",
        "src/victoruno/gui/main.py",
        "src/victoruno/integrations/__init__.py",
        "src/victoruno/integrations/chrome.py",
        "src/victoruno/integrations/documents.py",
        "src/victoruno/utils/__init__.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = root_dir / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests."""
    print("VictorUno Structure Test")
    print("=" * 40)
    
    tests = [
        test_file_structure,
        test_directory_structure,
        test_imports,
        test_configuration,
    ]
    
    all_passed = True
    for test in tests:
        try:
            result = test()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! VictorUno structure is correct.")
        return 0
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())