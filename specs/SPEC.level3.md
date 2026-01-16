meta {
    name = "CoachingAgent"
    version = "1.0"
    description = "Level 3: Planning Agent with Workflow"
}

system CoachingAgent {
    effect LLM {
        operation think(goal: String) -> String;
        operation decide(plan: String, context: String) -> String;
        operation reflect(reason: String) -> String;
        operation revise(plan: String) -> String;
    }
    
    effect User {
        operation listen() -> String;
        operation reply(message: String) -> String;
    }

    component Coach {
        description: "A coaching agent that plans, executes, and self-corrects.";
        
        state Session {
            goal: String
            plan: String
            history: List<String>
        }

        workflow StartSession(user_goal: String) {
            step Plan {
                perform LLM.think(user_goal)
            }
            
            step ExecuteLoop {
                perform User.listen()
            }
        }
    }
}