meta {
  name        = "CalculatorSystem"
  version     = "1.0"
  description = "A simple calculator with history tracking"
}

system CalculatorSystem {

    component Calculator {
        description: "Core calculation engine";
        
        state Memory {
            current_value: Float
            history: List<String>
        }

        invariant: "Division by zero is not allowed";

        function add(a: Float, b: Float) -> Float;
        function subtract(a: Float, b: Float) -> Float;
        function multiply(a: Float, b: Float) -> Float;
        function divide(a: Float, b: Float) -> Result<Float, String>;
        
        function clear() -> Unit;
        function get_history() -> List<String>;
    }
}