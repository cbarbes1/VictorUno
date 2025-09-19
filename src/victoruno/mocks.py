"""
Minimal mock implementations for testing without external dependencies.
"""

# Mock LangChain components
class BaseMessage:
    def __init__(self, content: str):
        self.content = content

class HumanMessage(BaseMessage):
    type = "human"

class AIMessage(BaseMessage):
    type = "ai"

class SystemMessage(BaseMessage):
    type = "system"

class ConversationBufferMemory:
    def __init__(self, return_messages=True):
        self.return_messages = return_messages
        self.messages = []
    
    def clear(self):
        self.messages = []

# Mock Ollama
class Ollama:
    def __init__(self, base_url, model, temperature=0.7):
        self.base_url = base_url
        self.model = model
        self.temperature = temperature

# Mock LangGraph components
class StateGraph:
    def __init__(self, state_class):
        self.state_class = state_class
        self.nodes = {}
        self.edges = {}
    
    def add_node(self, name, func):
        self.nodes[name] = func
    
    def add_edge(self, from_node, to_node):
        pass
    
    def add_conditional_edges(self, from_node, condition_func, mapping):
        pass
    
    def set_entry_point(self, node):
        pass
    
    def compile(self, checkpointer=None):
        return MockApp()

class MockApp:
    async def ainvoke(self, state, config=None):
        # Return a mock response
        return {
            "messages": [
                HumanMessage("Test message"),
                AIMessage("This is a mock response since external dependencies are not available.")
            ],
            "context": {},
            "documents": [],
            "web_content": None
        }

class MemorySaver:
    pass

END = "END"