from kernel.semantic_kernel import perform
from kernel.effects import Generate, LLMRequest

class Responder:
    def reply(self, query: str) -> str:
        if not query.strip():
            return ""
        
        user_msg = {"role": "user", "content": query}
        response = perform(Generate(LLMRequest(messages=[user_msg])))
        return response