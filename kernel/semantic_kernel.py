from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
from dataclasses import dataclass, replace, field
from abc import ABC, abstractmethod

# --- 1. Value Semantics (State) ---
@dataclass(frozen=True)
class State:
    pass

# --- 2. Algebraic Effects ---
T = TypeVar("T")

@dataclass
class Effect(Generic[T]):
    payload: Any

class EffectRequest(Exception):
    def __init__(self, effect: Effect, callback: Callable[[Any], Any]):
        self.effect = effect
        self.callback = callback

# Global runtime pointer for synchronous execution (e.g. in REPL)
_active_runtime = None

def perform(effect: Effect[T]) -> T:
    """
    Perform an effect. If an active runtime is set, it resolves it immediately.
    Otherwise, it raises EffectRequest for async/generator-based handling.
    """
    if _active_runtime:
        return _active_runtime._resolve_effect(effect)
    
    result = None
    def resume(val):
        nonlocal result
        result = val
    raise EffectRequest(effect, resume)
    return result # type: ignore

# --- 3. Handlers ---
class Handler(ABC):
    @abstractmethod
    def handle(self, effect: Effect) -> Any:
        pass

# --- 4. Agent Definition ---
@dataclass
class AgentSpec:
    name: str
    description: str
    invariants: List[Callable[[State], bool]] = field(default_factory=list)

class Agent(ABC):
    def __init__(self, spec: AgentSpec, initial_state: State):
        self.spec = spec
        self.state = initial_state

    @abstractmethod
    def policy(self) -> Any:
        pass