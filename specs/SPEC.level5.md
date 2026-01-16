meta {
    name = "MetaSolver"
    version = "1.0"
    description = "Level 5: Recursive Agent (The Holy Grail)"
}

system MetaSolver {
    effect System {
        # Spawns a new agent instance with fresh context
        operation recurse(spec: String, query: String) -> String;
    }

    component Orchestrator {
        description: "Solves complex problems by delegating to specialized sub-agents.";

        workflow SolveBigProblem(problem: String) {
            step Decompose {
                # In reality, LLM would decide which spec to use.
                # Here we hardcode delegating a math sub-problem to the CalculatorAgent.
                
                # "I need to calculate 25 * 4 as part of the big problem"
                sub_result = perform System.recurse("specs/SPEC.level2.md", "multiply 25 by 4")
            }
        }
    }
}
