from kernel.semantic_kernel import perform
from kernel.effects import Generate, LLMRequest

class Coach:
    def provide_feedback(self, performance_score: int) -> str:
        if performance_score >= 85:
            return "Great job! Keep up the good work!"
        elif performance_score < 40:
            return "It looks like you need some extra practice. Let's go over this again."
        else:
            return "Good effort, but there is room for improvement."

    def generate_training_plan(self, current_level: str, target_level: str) -> str:
        user_msg = f"Coach, I am currently at the {current_level} level and my goal is to reach the {target_level} level. Provide a plan starting with 'Step'."
        response = perform(Generate(LLMRequest(messages=[{"role": "user", "content": user_msg}])))
        return response
