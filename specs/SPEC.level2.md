meta {
    name = "CalculatorAgent"
    version = "1.0"
    description = "Level 2: Agent capable of using Math Tools via Effects"
}

system CalculatorAgent {
    effect Math {
        operation add(a: Float, b: Float) -> Float;
        operation sub(a: Float, b: Float) -> Float;
        operation mul(a: Float, b: Float) -> Float;
        operation div(a: Float, b: Float) -> Float;
    }

    component Solver {
        description: "Solves simple math problems using the Math effect.";

        function calculate(a: Float, b: Float, op: String) -> Float {
            perform Math.add(a, b)
        }
    }
}
