"""
Core functionality for VictorUno agent.
"""

import os
import sys
from langchain_core.tools import tool
from langchain_community.utilities.openweathermap import OpenWeatherMapAPIWrapper


class VictorUno:
    """
    Main VictorUno agent class for research, development, and optimization.
    """
    def __init__(
        self,
        name: str = "VictorUno",
        mode: str = "local",
        model: str = "gemma3:latest"
    ):
        """
        Initialize the VictorUno agent.

        Args:
            name (str): Name of the agent instance.
            mode (str): "local" for Ollama, "remote" for Anthropic.
            model (str): Model identifier.
                - For local: any Ollama model name (e.g., "llama3.1:8b", "gemma:latest").
                - For remote: Anthropic Claude model name (e.g., "claude-3-sonnet-20240229").
        """
        self.name = name
        self.version = "0.1.0"
        self.mode = mode
        self.model_name = model

        if mode == "remote":
            from langchain_anthropic import ChatAnthropic
            # Cloud model (Anthropic)
            self.llm = ChatAnthropic(
                model=model,
                temperature=0.3,
                max_tokens=512,
            )
        elif mode == "local":
            from langchain_ollama import ChatOllama
            # Local model (Ollama)
            self.llm = ChatOllama(
                model=model,
                temperature=0.3,
                num_predict=256,
            )
        else:
            raise ValueError(f"Invalid mode '{mode}', must be 'local' or 'remote'")
        
        weather = OpenWeatherMapAPIWrapper()
        
        # Define a tool from the wrapper
        @tool
        def weather_tool(location: str) -> str:
            """get the weather"""
            return weather.run(location)
        
        self.tools = [
            weather_tool
        ]
        
        self.llm = self.llm.bind_tools(self.tools)

    def weather(self, prompt: str)->str:
        """
        get Weather given a location

        Args:
            location (str): Location to check the weather

        Returns:
            str: The Weather report

        """
        output = self.llm.invoke(prompt)
        return output


        
    
    def research(self, topic: str) -> str:
        """
        Research a given topic.
        
        Args:
            topic (str): The topic to research
            
        Returns:
            str: Research results placeholder
        """
        prompt = f"""
        TASK:
        You are a concise description generator. 
        Given a single research topic as input, produce a clear, factual, and self-contained description. 
        Always answer directly and in complete sentences.

        STYLE & RESTRICTIONS:
        - Do not include disclaimers (e.g., "I cannot access external info").
        - Do not state limitations.
        - Base your answer only on your own knowledge.
        - Keep the description concise (2–4 sentences).
        - Use neutral, professional language.

        OUTPUT:
        Return only the description text. Do not add meta commentary or extra formatting.
        """
        messages = [
            ("system", prompt),
            ("user", topic)
        ]
        
        print("starting llm call")
        output = self.llm.invoke(messages)
        return f"Researching topic: {topic}\nDesciption: {output.content}"
    
    def develop(self, project: str) -> str:
        """
        Develop a project or solution.
        
        Args:
            project (str): The project to develop
            
        Returns:
            str: Development results placeholder
        """
        return f"Developing project: {project}"
    
    def optimize(self, target: str) -> str:
        """
        Optimize a given target system or process.
        
        Args:
            target (str): The target to optimize
            
        Returns:
            str: Optimization results placeholder
        """
        return f"Optimizing target: {target}"
    
    # def chat(self):
    #     while True:
    #         try:
    #             user_input = input("you> ").strip()
    #             if user_input.lower() in {"exit", "quit"}:
    #                 print("👋 Goodbye!")
    #                 break

    #             response = self.llm.invoke(user_input)
    #             # response may be an AIMessage or dict depending on backend
    #             if hasattr(response, "content"):
    #                 print(f"bot> {response.content}\n")
    #             else:
    #                 print(f"bot> {response}\n")

    #         except (KeyboardInterrupt, EOFError):
    #             print("\n👋 Goodbye!")
    #             sys.exit(0)
    
    def get_info(self) -> dict:
        """
        Get information about the agent.
        
        Returns:
            dict: Agent information
        """
        return {
            "name": self.name,
            "version": self.version,
            "capabilities": ["research", "develop", "optimize"]
        }