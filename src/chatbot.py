from typing import List
from kernel.semantic_kernel import perform
from kernel.effects import Generate, LLMRequest

class ChatBot:
    """A simple conversational agent with memory"""

    def __init__(self, persona: str) -> None:
        self.persona = persona
        self.history: List[str] = []

    def chat(self, user_message: str) -> str:
        """The core loop: Add user msg -> Call LLM -> Add response -> Return"""
        prompt = f"Persona: {self.persona}\nHistory: {self.history}\nUser: {user_message}"
        
        # Correctly call the Kernel Effect
        response = perform(Generate(LLMRequest(messages=[{"role": "user", "content": prompt}]))) 
        
        # The response is already a string, no need for indexing
        bot_response = str(response)
        
        self.history.append(f"User: {user_message}")
        self.history.append(f"Bot: {bot_response}")
        
        return bot_response

    def get_history(self) -> List[str]:
        """Returns the chat history"""
        return self.history
