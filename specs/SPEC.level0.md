meta {
    name = "StaticResponder"
    version = "1.0"
    description = "Level 0: Simple Input-Output Agent"
}

system StaticResponder {
    effect LLM {
        operation generate(prompt: String) -> String;
    }

    component Responder {
        description: "Responds to user queries using an LLM without maintaining state.";
        
        function reply(query: String) -> String {
            return perform LLM.generate(query)
        }
    }
}
