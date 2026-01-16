from kernel.semantic_kernel import perform
from kernel.effects import Math, MathOperation

class Solver:
    def calculate(self, a: float, b: float, op: str) -> float:
        return perform(Math(MathOperation(op=op, a=a, b=b)))
