meta {
    name = "ContextBot"
    version = "1.0"
    description = "Level 1: Context-Aware Agent"
}

system ContextBot {
    effect LLM {
        operation generate(prompt: String) -> String;
    }

    component Assistant {
        description: "Maintains conversation history and responds with context.";

        state Conversation {
            history: List<String>
        }

        function chat(message: String) -> String {
            # In a real implementation, this would append to history
            # and send the full context to the LLM.
            prompt = "History: " + str(state.history) + "\nUser: " + message
            response = perform LLM.generate(prompt)
            return response
        }
    }
}

