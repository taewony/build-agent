from typing import List
from kernel.semantic_kernel import perform
from kernel.effects import Generate, LLMRequest

class Assistant:
    def __init__(self):
        self.history: List[str] = []

    def chat(self, message: str) -> str:
        if not message.strip():
            return "Please provide a message."
        
        self.history.append(f"User: {message}")
        
        # Construct full context
        context = "\n".join(self.history)
        
        response = perform(Generate(LLMRequest(messages=[{"role": "user", "content": context}]))) 
        
        self.history.append(f"Assistant: {response}")
        return response
