"""
Command-line interface for VictorUno.
"""

import argparse
import sys
from .core import VictorUno


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="VictorUno - Personalized Agent to Research, Develop, and Optimize"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="VictorUno 0.1.0"
    )
    parser.add_argument(
        "command",
        choices=["research", "develop", "optimize", "info"],
        help="Command to execute"
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="Target for the command (required for research, develop, optimize)"
    )
    parser.add_argument(
        "--name",
        default="VictorUno",
        help="Name for the agent instance"
    )
    
    args = parser.parse_args()
    
    # Initialize the agent
    agent = VictorUno(name=args.name)
    
    # Execute the command
    if args.command == "info":
        info = agent.get_info()
        print(f"Agent: {info['name']}")
        print(f"Version: {info['version']}")
        print(f"Capabilities: {', '.join(info['capabilities'])}")
    else:
        if not args.target:
            print(f"Error: {args.command} command requires a target argument")
            sys.exit(1)
        
        if args.command == "research":
            result = agent.research(args.target)
        elif args.command == "develop":
            result = agent.develop(args.target)
        elif args.command == "optimize":
            result = agent.optimize(args.target)
        
        print(result)


if __name__ == "__main__":
    main()