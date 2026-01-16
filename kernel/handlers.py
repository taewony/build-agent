import os
import io
import sys
import litellm
import importlib.util
from typing import Dict, Any, Optional
from .semantic_kernel import Handler, Effect, perform
from .effects import Generate, ExecuteCode, ReadFile, WriteFile, Recurse, LLMRequest, Math, Listen, Reply, SendMessage, SubTask

# Safe Execution Imports (from recursive-llm wisdom)
from RestrictedPython import compile_restricted_exec, safe_globals, limited_builtins, utility_builtins
from RestrictedPython.Guards import guarded_iter_unpack_sequence, safer_getattr
from RestrictedPython.PrintCollector import PrintCollector

class LiteLLMHandler(Handler):
    def __init__(self, default_model: str = "qwen2.5:3b"):
        self.default_model = default_model

    def handle(self, effect: Effect) -> Any:
        if isinstance(effect, Generate):
            req: LLMRequest = effect.payload
            response = litellm.completion(
                model=req.model or self.default_model,
                messages=req.messages,
                stop=req.stop
            )
            return response.choices[0].message.content
        raise NotImplementedError

class SafeREPLHandler(Handler):
    """
    Highly secure Python REPL Handler inspired by recursive-llm.
    Uses RestrictedPython to prevent malicious or accidental system damage.
    """
    def __init__(self):
        self.env: Dict[str, Any] = {}
        self.max_output_chars = 2000

    def handle(self, effect: Effect) -> Any:
        if isinstance(effect, ExecuteCode):
            return self._execute_safe(effect.payload.code)
        raise NotImplementedError

    def _execute_safe(self, code: str) -> str:
        # Build restricted globals (The wisdom from recursive-llm)
        restricted_globals = safe_globals.copy()
        restricted_globals.update(limited_builtins)
        restricted_globals.update(utility_builtins)
        
        # Add guards
        restricted_globals['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
        restricted_globals['_getattr_'] = safer_getattr
        restricted_globals['_getitem_'] = lambda obj, index: obj[index]
        restricted_globals['_getiter_'] = iter
        restricted_globals['_print_'] = PrintCollector

        # Add safe modules
        import re, math, json
        restricted_globals.update({'re': re, 'math': math, 'json': json})

        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()

        try:
            byte_code = compile_restricted_exec(code)
            if byte_code.errors:
                return f"Compilation Error: {', '.join(byte_code.errors)}"

            exec(byte_code.code, restricted_globals, self.env)
            output = captured_output.getvalue()
            
            # Handle prints
            if '_print' in self.env and hasattr(self.env['_print'], 'txt'):
                output += ''.join(self.env['_print'].txt)

            if not output.strip():
                return "Executed successfully (no output)."
            
            return output[:self.max_output_chars]
        except Exception as e:
            return f"Runtime Error: {str(e)}"
        finally:
            sys.stdout = old_stdout

class FileSystemHandler(Handler):
    def handle(self, effect: Effect) -> Any:
        if isinstance(effect, ReadFile):
            with open(effect.payload.path, 'r', encoding='utf-8') as f:
                return f.read()
        elif isinstance(effect, WriteFile):
            os.makedirs(os.path.dirname(effect.payload.path), exist_ok=True)
            with open(effect.payload.path, 'w', encoding='utf-8') as f:
                f.write(effect.payload.content)
            return None
        raise NotImplementedError

class MathHandler(Handler):
    def handle(self, effect: Effect) -> Any:
        if isinstance(effect, Math):
            op = effect.payload.op
            a = effect.payload.a
            b = effect.payload.b
            if op == "add": return a + b
            if op == "sub": return a - b
            if op == "mul": return a * b
            if op == "div": return a / b if b != 0 else float('inf')
            raise ValueError(f"Unknown operation: {op}")
        raise NotImplementedError

class UserInteractionHandler(Handler):
    def __init__(self, input_queue: Optional[list] = None):
        self.input_queue = input_queue or []

    def handle(self, effect: Effect) -> Any:
        if isinstance(effect, Listen):
            if self.input_queue:
                return self.input_queue.pop(0)
            return "User provided no input (Mock)"
        if isinstance(effect, Reply):
            print(f"AGENTS SAYS: {effect.payload.message}")
            return "Replied"
        raise NotImplementedError

class MessageBusHandler(Handler):
    def handle(self, effect: Effect) -> Any:
        if isinstance(effect, SendMessage):
            msg = effect.payload
            prefix = "[BROADCAST]" if msg.broadcast else f"[TO: {msg.recipient}]"
            print(f"🚌 {prefix} {msg.content}")
            return "Sent"
        raise NotImplementedError

class RecursiveAgentHandler(Handler):
    """
    Handles the 'Recurse' effect by spawning a new isolated Runtime.
    This enables the "Level 5" capabilities.
    """
    def handle(self, effect: Effect) -> Any:
        if isinstance(effect, Recurse):
            task: SubTask = effect.payload
            spec_path = task.spec_path
            query = task.query
            
            print(f"🔄 [RecursiveHandler] Spawning Sub-Agent from '{spec_path}'...")
            print(f"    Goal: {query}")
            
            if not spec_path or not os.path.exists(spec_path):
                 return f"Error: Spec file '{spec_path}' not found."

            # 1. Compile the Spec (We reuse the Compiler via a fresh import or just use the file)
            # For simplicity, we assume the code is already built in 'src/' for now, 
            # OR we could trigger a build. Let's assume built for this prototype.
            
            # We need to find the component name from the spec to load the module
            # Ideally, we'd use the Compiler to parse it, but let's do a quick cheat or assume naming convention.
            # "SPEC.level2.md" -> system "CalculatorAgent" -> component "Solver" (we need to know this)
            
            # Let's map spec_path to module/class manually or use Compiler if available.
            # To be robust, let's look at the filename mapping we used:
            # SPEC.level2.md -> CalculatorAgent. 
            # We need to instantiate the Main Component. 
            # For Level 2, it is 'Solver' in 'src/solver.py'.
            
            # HACK: For the demo, we map:
            # specs/SPEC.level2.md -> src/solver.py, class Solver
            
            module_name = "solver"
            class_name = "Solver"
            method_name = "calculate" # The entry point? Or do we need a standard entry point?
            
            if "level2" in spec_path:
                module_name = "solver"
                class_name = "Solver"
                # Level 2 Solver needs specific args (a, b, op), but Recurse sends a string query.
                # The Sub-Agent needs an adapter or an LLM to parse the query into args.
                # This is why Level 5 usually needs a "Generalist" sub-agent or the sub-agent needs a "Natural Language Interface".
                
                # Let's SIMULATE the Sub-Agent's "Thinking" phase here to parse the query.
                # In a real impl, the Sub-Agent would have a 'workflow' that accepts a string.
                # Since Level 2 Solver is a "Tool", let's wrap it.
                
                if "multiply" in query:
                    import re
                    nums = [float(s) for s in re.findall(r'-?\d+', query)]
                    if len(nums) >= 2:
                        # Instantiate Runtime
                        from .runtime import Runtime
                        import kernel.semantic_kernel as sk
                        
                        # ISOLATION: New Runtime
                        sub_runtime = Runtime()
                        sub_runtime.register_handler(MathHandler()) # Give it Math skills
                        # It doesn't need Recurse handler unless it recurses too (Fractal!)
                        
                        # We need to execute the component method inside this runtime context
                        # We temporarily switch the global context or pass it?
                        # Our 'perform' uses '_active_runtime'. We must swap it.
                        
                        parent_runtime = sk._active_runtime
                        sk._active_runtime = sub_runtime
                        
                        try:
                            # Load Module
                            import importlib.util
                            module_path = os.path.join("src", f"{module_name}.py")
                            spec = importlib.util.spec_from_file_location(class_name, module_path)
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            cls = getattr(module, class_name)
                            agent_instance = cls()
                            
                            # Run Logic
                            result = agent_instance.calculate(a=nums[0], b=nums[1], op="mul")
                            return str(result)
                            
                        except Exception as e:
                            return f"Sub-Agent Crashed: {e}"
                        finally:
                            # Restore Parent Context
                            sk._active_runtime = parent_runtime
            
            return "Error: Could not determine how to run sub-agent."
            
        raise NotImplementedError
