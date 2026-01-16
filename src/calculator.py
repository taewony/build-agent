from typing import List, Union

class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a: float, b: float) -> float:
        result = a + b
        self.history.append(f"add({a}, {b}) = {result}")
        return result

    def subtract(self, a: float, b: float) -> float:
        result = a - b
        self.history.append(f"subtract({a}, {b}) = {result}")
        return result

    def multiply(self, a: float, b: float) -> float:
        result = a * b
        self.history.append(f"multiply({a}, {b}) = {result}")
        return result

    def divide(self, a: float, b: float) -> Union[float, str]:
        if b == 0:
            return "Division by zero is not allowed"
        result = a / b
        self.history.append(f"divide({a}, {b}) = {result}")
        return result

    def clear(self) -> None:
        self.history.clear()

    def get_history(self) -> List[str]:
        return self.history