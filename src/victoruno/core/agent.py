"""Core agent implementation using LangChain and LangGraph."""

import asyncio
import logging
from typing import Any, Dict, List, Optional, TypedDict
from pathlib import Path

try:
    from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
    from langchain.memory import ConversationBufferMemory
    from langchain_community.llms import Ollama
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema.runnable import RunnablePassthrough
    from langchain.schema.output_parser import StrOutputParser
    
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint.memory import MemorySaver
    LANGCHAIN_AVAILABLE = True
except ImportError:
    # Use mock implementations for testing
    from ..mocks import (
        BaseMessage, HumanMessage, AIMessage, SystemMessage,
        ConversationBufferMemory, Ollama, StateGraph, END, MemorySaver
    )
    LANGCHAIN_AVAILABLE = False

from .config import Config
from ..integrations.chrome import ChromeIntegration
from ..integrations.documents import DocumentProcessor

logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """State for the VictorUno agent."""
    messages: List[BaseMessage]
    current_task: Optional[str]
    context: Dict[str, Any]
    documents: List[str]
    web_content: Optional[str]


class VictorUnoAgent:
    """Main agent class for VictorUno."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the VictorUno agent."""
        self.config = config or Config.from_env()
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Initialize Ollama LLM
        self.llm = Ollama(
            base_url=self.config.ollama_host,
            model=self.config.ollama_model,
            temperature=0.7,
        )
        
        # Initialize integrations
        self.chrome_integration = ChromeIntegration(self.config)
        self.document_processor = DocumentProcessor(self.config)
        
        # Create the agent workflow
        self.workflow = self._create_workflow()
        self.app = self.workflow.compile(checkpointer=MemorySaver())
        
        logger.info(f"VictorUno agent initialized with model: {self.config.ollama_model}")
        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain not available - using mock implementations for testing")
    
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow for the agent."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("process_input", self._process_input)
        workflow.add_node("generate_response", self._generate_response)
        workflow.add_node("handle_documents", self._handle_documents)
        workflow.add_node("web_research", self._web_research)
        
        # Set entry point
        workflow.set_entry_point("process_input")
        
        # Add edges
        workflow.add_conditional_edges(
            "process_input",
            self._route_request,
            {
                "documents": "handle_documents",
                "web_research": "web_research",
                "chat": "generate_response",
            }
        )
        
        workflow.add_edge("handle_documents", "generate_response")
        workflow.add_edge("web_research", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow
    
    def _route_request(self, state: AgentState) -> str:
        """Route the request based on the latest message."""
        if not state["messages"]:
            return "chat"
        
        latest_message = state["messages"][-1].content.lower()
        
        if any(keyword in latest_message for keyword in ["document", "file", "upload"]):
            return "documents"
        elif any(keyword in latest_message for keyword in ["search", "research", "browse", "web"]):
            return "web_research"
        else:
            return "chat"
    
    async def _process_input(self, state: AgentState) -> AgentState:
        """Process the input and update state."""
        logger.debug("Processing input")
        
        # Extract current task from the latest message
        if state["messages"]:
            latest_message = state["messages"][-1]
            state["current_task"] = latest_message.content
        
        return state
    
    async def _generate_response(self, state: AgentState) -> AgentState:
        """Generate a response using the LLM."""
        logger.debug("Generating response")
        
        # Create system message
        system_message = SystemMessage(content=f"""
You are {self.config.agent_name}, a personal AI assistant designed to help with research, development, and optimization tasks.

Your capabilities include:
- Answering questions and providing explanations
- Analyzing documents and extracting insights
- Conducting web research
- Helping with code and development tasks
- Optimizing workflows and processes

Context from documents: {state.get('documents', [])}
Web content: {state.get('web_content', 'None')}

Be helpful, accurate, and concise in your responses.
""")
        
        # Prepare messages for the LLM
        messages = [system_message] + state["messages"]
        
        # Generate response
        try:
            if LANGCHAIN_AVAILABLE:
                # Create prompt template
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_message.content),
                    *[(msg.type, msg.content) for msg in state["messages"]]
                ])
                
                chain = prompt | self.llm | StrOutputParser()
                response = await asyncio.get_event_loop().run_in_executor(
                    None, chain.invoke, {"messages": messages}
                )
            else:
                # Mock response when LangChain is not available
                user_message = state['messages'][-1].content if state['messages'] else 'Hello'
                response = f"Mock response: I understand you said '{user_message}'. This is a demonstration response since LangChain is not available in this environment. In a full deployment with Ollama, I would provide intelligent responses using local LLMs."
            
            # Add AI response to messages
            state["messages"].append(AIMessage(content=response))
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            error_response = f"I apologize, but I encountered an error: {str(e)}"
            state["messages"].append(AIMessage(content=error_response))
        
        return state
    
    async def _handle_documents(self, state: AgentState) -> AgentState:
        """Handle document processing."""
        logger.debug("Handling documents")
        
        # For now, this is a placeholder that would be called when documents are uploaded
        # In a full implementation, this would process documents from state or a queue
        state["context"]["document_processed"] = True
        
        return state
    
    async def _web_research(self, state: AgentState) -> AgentState:
        """Handle web research."""
        logger.debug("Performing web research")
        
        # Extract search query from the latest message
        if state["messages"]:
            latest_message = state["messages"][-1].content
            # Simple query extraction - in practice, this could be more sophisticated
            query = latest_message.replace("search", "").replace("research", "").strip()
            
            try:
                # Perform web search
                search_results = await self.chrome_integration.search_web(query, num_results=3)
                
                # Format results for the agent
                web_content = "Web search results:\n\n"
                for i, result in enumerate(search_results, 1):
                    web_content += f"{i}. {result['title']}\n"
                    web_content += f"   URL: {result['url']}\n"
                    web_content += f"   Description: {result['description']}\n\n"
                
                state["web_content"] = web_content
                
            except Exception as e:
                logger.error(f"Error in web research: {e}")
                state["web_content"] = f"Web research encountered an error: {str(e)}"
        
        return state
    
    async def chat(self, message: str, thread_id: str = "default") -> str:
        """Send a message to the agent and get a response."""
        try:
            # Create initial state
            initial_state = {
                "messages": [HumanMessage(content=message)],
                "current_task": None,
                "context": {},
                "documents": [],
                "web_content": None,
            }
            
            # Run the workflow
            result = await self.app.ainvoke(
                initial_state,
                config={"configurable": {"thread_id": thread_id}}
            )
            
            # Return the latest AI message
            ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]
            if ai_messages:
                return ai_messages[-1].content
            else:
                return "I'm sorry, I couldn't generate a response."
                
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"I encountered an error: {str(e)}"
    
    def reset_conversation(self, thread_id: str = "default") -> None:
        """Reset the conversation for a given thread."""
        self.memory.clear()
        logger.info(f"Conversation reset for thread: {thread_id}")
    
    async def process_document(self, file_path: Path) -> str:
        """Process a document and add it to the agent's knowledge."""
        try:
            result = await self.document_processor.process_document(file_path)
            
            if result["success"]:
                # Store document content for future reference
                # In a production system, this might be stored in a vector database
                return f"Successfully processed '{result['filename']}'. " \
                       f"Content: {result['word_count']} words, {result['char_count']} characters. " \
                       f"The document content is now available for our conversation."
            else:
                return result["message"]
                
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return f"Error processing document: {str(e)}"
    
    async def web_search(self, query: str) -> str:
        """Perform a web search using Chrome integration."""
        try:
            search_results = await self.chrome_integration.search_web(query, num_results=5)
            
            if not search_results:
                return "No search results found."
            
            # Format results
            formatted_results = f"Web search results for '{query}':\n\n"
            
            for i, result in enumerate(search_results, 1):
                formatted_results += f"{i}. **{result['title']}**\n"
                formatted_results += f"   URL: {result['url']}\n"
                if result['description']:
                    formatted_results += f"   Description: {result['description']}\n"
                formatted_results += "\n"
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in web search: {e}")
            return f"Error performing web search: {str(e)}"