# SPAK: Spec-Driven Programmable Agent Kernel
## The Operating System for Agentic AI Education

**"From Prompting to Programming: A Formal Kernel for Verifiable Agents"**

SPAK is a **Programmable Agent Kernel** designed to teach and enforce rigorous engineering practices in AI Agent development. Unlike frameworks that focus on "chaining prompts," SPAK treats Agent Logic as a formal artifact that must be **compiled from a Specification (AgentSpec)**, **verified against Invariants**, and **executed within an Effect-Isolated Runtime**.

This project serves as a reference implementation for **"Agent Engineering"** as an academic discipline, providing a structured curriculum from simple functions to recursive, self-improving systems.

---

## 🏗 Core Architecture

> **"An Agent is an Endofunctor on a Semantic Category."**

SPAK operates on three fundamental pillars:

1.  **Semantic Specification (AgentSpec):** A Domain-Specific Language (DSL) that defines the agent's **State Space** (Category) and **Transitions** (Morphisms), not just its prompts.
2.  **Algebraic Effect Runtime:** Separates **Policy** (LLM Decisions) from **Mechanism** (IO/Tools). The Agent *requests* an effect; the Kernel *decides* how to handle it (Execute, Mock, or Deny).
3.  **Recursive Fractal Design:** The system is capable of infinite scalability via **Recursive Sub-Kernels**. A parent agent can spawn an isolated child agent to solve a sub-problem with a fresh context window.

---

## 📚 The Agent Curriculum (Maturity Levels)

SPAK implements a graded curriculum to demonstrate the evolution of agent complexity. All levels are implemented and verifiable in this repository.

| Level | Agent Type | Key Concept | Spec File | Status |
| :--- | :--- | :--- | :--- | :--- |
| **0** | **Static Responder** | Input $\to$ Output | `specs/SPEC.level0.md` | ✅ Ready |
| **1** | **Context-Aware Bot** | State Persistence | `specs/SPEC.level1.md` | ✅ Ready |
| **2** | **Tool-Use Agent** | Algebraic Effects (Math) | `specs/SPEC.level2.md` | ✅ Ready |
| **3** | **Planning Agent** | Workflows (Loops) | `specs/SPEC.level3.md` | ✅ Ready |
| **4** | **Multi-Agent System** | Collaboration (MsgBus) | `specs/SPEC.level4.md` | ✅ Ready |
| **5** | **Recursive Solver** | Isolation (Sub-Kernel) | `specs/SPEC.level5.md` | ✅ Ready |

### Understanding Agent Maturity

The levels below define the pedagogical path from simple prompt-based automation to advanced autonomous systems:

*   **Level 0: Stimulus-Response (Capability: Pure Functions)**
    The agent maps a single input to a single output. It has no memory and no side effects.
    *   *Concept:* **Morphism** - A transformation between states.
*   **Level 1: Context-Aware (Capability: State Management)**
    The agent remembers previous turns. It can maintain a conversation history or an internal mental model.
    *   *Concept:* **Objects** - Immutable snapshots of semantic state.
*   **Level 2: Tool-Enabled (Capability: Algebraic Effects)**
    The agent can interact with the external world (Calculators, Search APIs, File Systems) via explicit, kernel-mediated requests.
    *   *Concept:* **Side-Effect Isolation** - Decoupling logic from execution.
*   **Level 3: Goal-Oriented (Capability: Workflows)**
    The agent can plan multiple steps, use loops, and self-correct based on feedback.
    *   *Concept:* **Endofunctor** - A mapping that preserves the structure of the semantic category while iterating.
*   **Level 4: Collaborative (Capability: Multi-Agent Systems)**
    Multiple specialized components (e.g., Manager and Worker) communicate through a shared Message Bus to achieve a complex goal.
    *   *Concept:* **Category Composition** - Building complex systems from simpler, verified components.
*   **Level 5: Recursive (Capability: Fractal Scalability)**
    The "Holy Grail." Agents can spawn entirely new Kernel instances (Sub-Kernels). This bypasses LLM context limits and ensures fault-tolerant isolation.
    *   *Concept:* **Recursive Kernel** - The ability of the system to define and run instances of itself.

---

## 🛠 Usage & Workflow

The system runs a **REPL-driven Build Loop**:

```bash
# 1. Start the Kernel Shell
$ python spak.py

# 2. Load a Specification (e.g., Level 3 Planning Agent)
(kernel) > load specs/SPEC.level3.md
[Kernel] Loaded System: CoachingAgent

# 3. Auto-Implement (The Builder Agent synthesizes code from Spec)
(kernel) > build
[Builder] Generating tests for 'Coach'...
[Builder] Synthesizing implementation for 'Coach'...
✅ Synthesized src/coach.py

# 4. Verify Behavior (The Verifier runs the tests)
(kernel) > verify
[Static Analysis] Starting verification for system: CoachingAgent
[Dynamic Analysis] Running tests from: tests/tests.coach.yaml
  🧪 Running test_standard_success... ✅ PASS
  🧪 Running test_workflow_steps... ✅ PASS
[Result] Verification PASSED.
```

---

## 🌍 Why "Kernel"?

In Computer Science, a **Kernel** manages resources, provides abstraction, and enforces isolation. SPAK does exactly this for Agents:

1.  **Resource Management:** Manages the **Context Window** as a scarce resource (via Recursion/Memory).
2.  **Isolation:** Protects the host system by sandboxing **Effect Execution** (e.g., `SafeREPLHandler`).
3.  **Abstraction:** Provides a standard Syscall interface (`perform Effect`) for LLMs, replacing fragile prompt engineering.

---



## 📚 References & Pedagogical Roots



SPAK is inspired by and expands upon the foundational concepts found in the **[ML105: Agentic AI](https://github.com/rdali/ML105_Agents)** curriculum. 



### Comparison: ML105 vs. SPAK



While ML105 provides an excellent introduction to building agents using standard libraries (LangChain, Bedrock), SPAK reframes these lessons into a formal **Agent Engineering** framework:



| ML105 Stage | SPAK Maturity Level | Enhancement in SPAK |

| :--- | :--- | :--- |

| `1-llm_call.py` | **Level 0 (Morphism)** | Defined via formal `function` in `AgentSpec`. |

| `3-agent_simple.py` | **Level 2 (Effects)** | Tools are **Algebraic Effects** mediated by the Kernel. |

| `4-agent_memory.py` | **Level 1 (State)** | Memory is modeled as an **Immutable Semantic State**. |

| `7-architecture.ipynb`| **Level 4 (Collaboration)**| Uses a formal **Message Bus** effect for inter-agent comms. |

| (README Loop) | **Level 3 (Workflow)** | Expressed as **Turing-complete workflows** in the Spec. |

| (N/A) | **Level 5 (Recursion)** | SPAK introduces **Recursive Sub-Kernels** for infinite scaling. |



By moving from "scripts" to "specs," SPAK ensures that every stage of the agent's evolution is verifiable, replayable, and architecturally sound.
It can be positioned as a next-generation **"Universal Agent Factory"** for both education and production engineering.


---



## 📝 Citation



If you use SPAK for research or education, please cite:



> **"SPAK: A Formally Verified, Spec-Driven Kernel for Curriculum-Based AI Agent Synthesis"** (Draft, 2026)
