from kernel.semantic_kernel import perform
from kernel.effects import SendMessage, Message

class Manager:
    def __init__(self):
        self.team_members = {}

    def add_team_member(self, member_name: str, role: str) -> str:
        if not role:
            return "Error: Role cannot be empty"
        self.team_members[member_name] = role
        return f"Member {member_name} added as {role}"

    def assign_task(self, task: str, member_name: str) -> str:
        if member_name in self.team_members:
            # Use MessageBus to delegate
            perform(SendMessage(Message(recipient=member_name, content=task)))
            return f"Task '{task}' assigned to {member_name}"
        else:
            return f"Error: Member {member_name} not found"
