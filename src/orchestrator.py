from kernel.semantic_kernel import perform
from kernel.effects import Recurse, SubTask

class Orchestrator:
    def solve_big_problem(self, problem: str) -> str:
        # In a real system, the agent would parse the problem.
        # Here we hardcode the recursion to demonstrate the capability.
        
        # "I need to calculate 25 * 4 as part of the big problem"
        print(f"[Orchestrator] Delegating part of '{problem}' to Sub-Agent...")
        
        sub_result = perform(Recurse(SubTask(
            spec_path="specs/SPEC.level2.md",
            query="multiply 25 by 4",
            context="part of bigger problem"
        )))
        
        return f"Solved: {sub_result}"
