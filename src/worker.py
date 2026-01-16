from kernel.semantic_kernel import perform
from kernel.effects import SendMessage, Message

class Worker:
    def do_work(self, task: str) -> str:
        if not task:
            return 'empty_list_error'
        
        # In collaborative mode, worker might reply back
        result = task # Identity for test matching
        perform(SendMessage(Message(recipient="Manager", content=f"Finished {task}")))
        return result
