# Future Roadmap & Paper Strategy for SPAK

**Strategic Shift:**
- **Naming:** Renamed from `SBAK` (Spec-Driven Build-Agent Kernel) to **SPAK** (Spec-Driven Programmable Agent Kernel).
- **Paper Focus:** Shift from "Performance/SOTA beating" to **"Educational & Foundational Contribution"**.
  - **Core Argument:** SPAK enables a structured, curriculum-based approach to learning AI Engineering (from simple functions to complex autonomous systems) without reliance on opaque cloud frameworks.
  - **Target Audience:** Academic educators, AI engineering researchers.

---

## Part 1. Academic Paper Refinement (Target: KAIS / ICSE)

### 1.1 Current Status
- **Structural soundness:** The SPAK architecture is solid.
- **Formalism:** `AgentSpec` has been formalized using Category Theory (See `whitepaper/AgentSpec.md`).
- **Kernel Definition:** `SPAK` kernel specification is established (See `whitepaper/SPAK_Kernel.md`).

### 1.2 Execution Plan (Critical To-Dos)

#### 1. [x] Formalize AgentSpec DSL
- **Status:** Complete.
- **Outcome:** Reframed agents as *Endofunctors on Semantic Categories*. This provides the theoretical backbone for the paper.

#### 2. [ ] Comparative Case Study: The "Agent Curriculum"
- **Goal:** Demonstrate SPAK's utility in education by implementing the "ML105 Agent Maturity Levels" using `AgentSpec`.
- **Reference:** https://github.com/rdali/ML105_Agents
- **Implementation Plan:**
    - **Level 0 (Static):** Implement `StaticResponder` (Input -> Output).
    - **Level 1 (Context):** Implement `ContextAwareBot` (State: History).
    - **Level 2 (Tool Use):** Implement `CalculatorAgent` (Effect: ToolCall). ✅ **Completed**
    - **Level 3 (Planning):** Implement `CoachingAgent` (Workflow: Plan -> Act).
    - **Level 4 (Multi-Agent):** Implement `TeamCoordinator` (System composition).
- **Paper Argument:** "SPAK allows students to transition from Level N to N+1 by simply adding semantic constructs (e.g., adding `state` or `effects`) to the spec, whereas traditional coding requires massive refactoring."

#### 3. [ ] Cost & Benefit Analysis
- **Metric:** "Lines of Implementation Logic" vs "Lines of Specification".
- **Argument:** "The Specification overhead pays off by automating 80% of the boilerplate (Runtime, Effect handling, State persistence)."

---

## Part 2. Evolution to a "Programmable Agent Kernel"

To support the above curriculum, the Kernel needs specific enhancements.

### 2.1 Dynamic Workflow Specification
- **Need:** Level 3 agents require loops and conditionals.
- **Action:** Implement `loop`, `if/else`, and `until` in the Compiler/Builder.
    ```aispec
    workflow Solve {
        step plan = perform LLM.think(goal)
        loop until plan.is_complete {
            step action = perform LLM.decide(plan)
        }
    }
    ```

### 2.2 Hierarchical Memory Management
- **Need:** Level 2+ agents run out of context.
- **Action:** Implement `MemoryManager` component in the standard library.
    ```aispec
    component Memory {
        state {
            short_term : List<Msg> @limit(10)
            long_term  : VectorStore
        }
    }
    ```

### 2.3 Meta-Control (Intents)
- **Need:** High-level abstraction for complex tasks.
- **Action:** Introduce `transform` primitive to abstract prompt engineering.

### 2.4 Self-Evolving Kernel (The "Singularity" Test)
- **Concept:** The SPAK Kernel reads `SPEC.spak.md` and rebuilds its own `runtime.py`.
- **Goal:** Prove the system is "Turing Complete" in the domain of Agent Construction.

---

## Part 3. Immediate Next Steps

1.  **Refactor Compiler:** Update `kernel/compiler.py` to support the v0.4 syntax defined in `whitepaper/AgentSpec.md`.
2. [x] Implement Level 0-1: Created `specs/SPEC.level0.md` and `specs/SPEC.level1.md` and verified they build correctly.
3.  **Paper Draft:** Update `docs/paper.md` with the new "Educational" positioning and Formal definitions.
