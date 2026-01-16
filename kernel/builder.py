import os
import litellm
from typing import Optional, Any
from .compiler import ComponentSpec

class Builder:
    """
    The 'Coder' component.
    Synthesizes Python implementation from ComponentSpec AST.
    """
    def __init__(self, model_name: str = "ollama/qwen2.5-coder:7b", temperature: float = 0.1):
        self.model_name = model_name
        self.temperature = temperature
        self.conversation_history = [] # Stores {type, prompt, response}

    def get_history(self) -> list:
        return self.conversation_history

    def implement_component(self, spec: ComponentSpec, context_info: str = "") -> str:
        """
        Calls LLM to generate Python code for a given ComponentSpec.
        """
        prompt = self._construct_implement_prompt(spec, context_info)
        
        print(f"🤖 [Builder] Synthesizing implementation for '{spec.name}' using {self.model_name}...")
        
        try:
            # Enable Streaming
            response = litellm.completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an expert Python engineer specialized in Spec-Driven Development. Your task is to implement Python classes that strictly match the provided Formal Specification (AISpec)."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                stream=True
            )
            
            full_content = ""
            print("    📝 Generating: ", end="", flush=True)
            
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                full_content += content
                print(content, end="", flush=True)
            
            print("\n") # Newline after completion
            
            result_code = self._extract_code(full_content)
            self.conversation_history.append({
                "type": "implement",
                "component": spec.name,
                "prompt": prompt,
                "response": full_content
            })
            return result_code
        
        except Exception as e:
            error_msg = str(e)
            if "Connection refused" in error_msg or "11434" in error_msg:
                return "# Error: Could not connect to Ollama.\n# ACTION: Please run 'ollama serve --host 127.0.0.1 --port 11434' in another terminal."
            return f"# Error during synthesis: {error_msg}"

    def fix_implementation(self, code: str, error_log: str) -> str:
        """
        Repairs existing code based on verification errors.
        """
        print(f"🛠️ [Builder] Repairing implementation...")
        prompt = f"""The following Python code failed verification. Fix the code to satisfy the specification and resolve the errors.

CODE:
{code}

ERROR LOG:
{error_log}

CRITICAL INSTRUCTIONS:
1. Output the FULL corrected Python file content.
2. Wrap the code inside a single ```python code block.
3. DO NOT write any explanations, suggestions, or conversational text.
4. Just give me the file content.
"""
        
        try:
            response = litellm.completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a silent code repair machine. Output only the requested Python code."},
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )
            
            full_content = ""
            print("    🔧 Fixing: ", end="", flush=True)
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                full_content += content
                print(content, end="", flush=True)
            print("\n")

            result_code = self._extract_code(full_content)
            self.conversation_history.append({
                "type": "fix_implementation",
                "prompt": prompt,
                "response": full_content
            })
            return result_code
        except Exception as e:
            if "Connection refused" in str(e) or "11434" in str(e):
                print("❌ [Builder] Connection to Ollama failed.")
            return code # Return original if fix fails

    def generate_tests(self, spec: ComponentSpec, system_name: str) -> str:
        """
        Synthesizes YAML test vectors from ComponentSpec.
        """
        print(f"🧪 [Builder] Generating test vectors for '{spec.name}'...")
        
        funcs_str = "\n".join([f"  - {f.name}(...)" for f in spec.functions])
        invariants_str = "\n".join([f"  * {i}" for i in spec.invariants])

        prompt = f"""Generate a YAML test specification for the following component:

SYSTEM: {system_name}
COMPONENT: {spec.name}

FUNCTIONS:
{funcs_str}

INVARIANTS:
{invariants_str}

REQUIREMENTS:
1. Output ONLY valid YAML.
2. Structure must be:
   system: {system_name}
   component: {spec.name}
   tests:
     - name: test_name
       function: func_name
       input: {{arg: val}}
       expected: result
3. Create at least 3 tests:
   - A standard success case
   - An edge case (e.g. division by zero, empty list)
   - A workflow case (multiple steps) if applicable.
"""
        try:
            response = litellm.completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a QA Engineer. Generate YAML test vectors to verify the component logic."},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
                temperature=0.3
            )
            
            full_content = ""
            print("    📝 Writing Tests: ", end="", flush=True)
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                full_content += content
                print(content, end="", flush=True)
            print("\n")
            
            yaml_result = ""
            if "```yaml" in full_content:
                yaml_result = full_content.split("```yaml")[1].split("```")[0].strip()
            elif "```" in full_content:
                yaml_result = full_content.split("```")[1].split("```")[0].strip()
            else:
                yaml_result = full_content.strip()
            
            self.conversation_history.append({
                "type": "generate_tests",
                "component": spec.name,
                "prompt": prompt,
                "response": full_content
            })
            return yaml_result

        except Exception as e:
            if "Connection refused" in str(e) or "11434" in str(e):
                return "# Error: Could not connect to Ollama.\n# ACTION: Please run 'ollama serve --host 127.0.0.1 --port 11434' in another terminal."
            return f"# Error generating tests: {str(e)}"

    def fix_tests(self, yaml_content: str, error_log: str) -> str:
        """
        Repairs broken YAML test vectors based on execution errors.
        """
        print(f"🧬 [Builder] Repairing test vectors...")
        
        prompt = f"""The following YAML test file caused execution errors. Fix the test inputs to match the actual function signatures implied by the errors.

BROKEN YAML:
{yaml_content}

ERROR LOG:
{error_log}

CRITICAL INSTRUCTIONS:
1. Output the FULL corrected YAML file content.
2. Wrap the YAML inside a single ```yaml code block.
3. DO NOT write any explanations, suggestions, or conversational text.
4. Just give me the file content.
"""
        try:
            response = litellm.completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a silent code repair machine. Output only the requested YAML."},
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )
            
            full_content = ""
            print("    📝 Rewrite Tests: ", end="", flush=True)
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                full_content += content
                print(content, end="", flush=True)
            print("\n")
            
            if "```yaml" in full_content:
                result_yaml = full_content.split("```yaml")[1].split("```")[0].strip()
            elif "```" in full_content:
                result_yaml = full_content.split("```")[1].split("```")[0].strip()
            else:
                result_yaml = full_content.strip()

            self.conversation_history.append({
                "type": "fix_tests",
                "prompt": prompt,
                "response": full_content
            })
            return result_yaml

        except Exception as e:
            return yaml_content # Return original if fail

    def _construct_implement_prompt(self, spec: ComponentSpec, context_info: str) -> str:
        # Convert AST back to a readable string for LLM
        funcs = []
        for f in spec.functions:
            params = ", ".join([f"{p.name}: {p.type.name}" for p in f.params])
            funcs.append(f"  - {f.name}({params}) -> {f.return_type.name}")
        
        funcs_str = "\n".join(funcs)
        invariants_str = "\n".join([f"  * {i}" for i in spec.invariants])

        # Check for Effect usage hints
        effect_instructions = """
CRITICAL REQUIREMENT: This component uses Effects (like LLM or FileIO). 
YOU MUST USE THE KERNEL'S EFFECT SYSTEM AS FOLLOWS:
1. Import perform: `from kernel.semantic_kernel import perform`
2. Import Effect types: `from kernel.effects import Generate, LLMRequest` (or others as needed)
3. To call LLM: `response = perform(Generate(LLMRequest(messages=[{"role": "user", "content": user_msg}])))`
DO NOT SIMULATE THE EFFECT. YOU MUST CALL THE PERFORM FUNCTION.
"""

        prompt = f"""Generate a Python implementation for the following component specification:

COMPONENT: {spec.name}
DESCRIPTION: {spec.description}

FUNCTIONS TO IMPLEMENT:
{funcs_str}

INVARIANTS/CONSTRAINTS:
{invariants_str}

{context_info}

REQUIREMENTS:
1. Return ONLY the Python code inside a code block.
2. Use standard Python type hints.
3. The class name MUST be exactly '{spec.name}'.
4. Do not include external dependencies unless necessary.
5. If the implementation is a core part of the system, keep it concise and robust.
{effect_instructions}
"""
        return prompt

    def _extract_code(self, text: str) -> str:
        """Extracts code from markdown blocks if present."""
        if "```python" in text:
            return text.split("```python")[1].split("```")[0].strip()
        if "```" in text:
            return text.split("```")[1].split("```")[0].strip()
        return text.strip()
