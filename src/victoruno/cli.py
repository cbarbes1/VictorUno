"""Command-line interface for VictorUno."""

import asyncio
import argparse
import sys
import logging
from pathlib import Path

from ..core.agent import VictorUnoAgent
from ..core.config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VictorUnoCLI:
    """Command-line interface for VictorUno."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.config = Config.from_env()
        self.agent = VictorUnoAgent(self.config)
    
    async def interactive_chat(self):
        """Start an interactive chat session."""
        print(f"🤖 {self.config.agent_name} - Personal AI Assistant")
        print("Type 'quit', 'exit', or 'bye' to end the conversation.")
        print("Type 'reset' to clear the conversation history.")
        print("-" * 50)
        
        thread_id = "cli_session"
        
        while True:
            try:
                user_input = input("\n🧑 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'reset':
                    self.agent.reset_conversation(thread_id)
                    print("\n🔄 Conversation reset.")
                    continue
                
                print("\n🤖 VictorUno: ", end="", flush=True)
                response = await self.agent.chat(user_input, thread_id)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error in interactive chat: {e}")
                print(f"\n❌ Error: {e}")
    
    async def single_query(self, query: str):
        """Process a single query and exit."""
        try:
            response = await self.agent.chat(query)
            print(response)
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            print(f"Error: {e}")
            sys.exit(1)
    
    async def process_document(self, file_path: str):
        """Process a document."""
        try:
            path = Path(file_path)
            if not path.exists():
                print(f"Error: File '{file_path}' not found.")
                sys.exit(1)
            
            result = await self.agent.process_document(path)
            print(result)
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            print(f"Error: {e}")
            sys.exit(1)


async def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="VictorUno - Personal AI Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  victoruno                          # Start interactive chat
  victoruno --query "What is AI?"    # Single query
  victoruno --document file.pdf      # Process document
  victoruno --web                    # Start web interface
  victoruno --gui                    # Start GUI interface
        """
    )
    
    parser.add_argument(
        "--query", "-q",
        help="Send a single query and exit"
    )
    parser.add_argument(
        "--document", "-d",
        help="Process a document file"
    )
    parser.add_argument(
        "--web", "-w",
        action="store_true",
        help="Start web interface"
    )
    parser.add_argument(
        "--gui", "-g",
        action="store_true",
        help="Start GUI interface"
    )
    parser.add_argument(
        "--config",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    cli = VictorUnoCLI()
    
    if args.web:
        from ..web.main import run_web_server
        await run_web_server()
    elif args.gui:
        from ..gui.main import run_gui
        run_gui()
    elif args.query:
        await cli.single_query(args.query)
    elif args.document:
        await cli.process_document(args.document)
    else:
        await cli.interactive_chat()


if __name__ == "__main__":
    asyncio.run(main())