# SPAK: A Spec-Driven Programmable Agent Kernel for AI Engineering Education

## 1. Value Proposition (Educational & Foundational)

**Conclusion: High Impact for AI Engineering Pedagogy**

While most agent research focuses on performance metrics (e.g., SWE-bench), **SPAK (Spec-Driven Programmable Agent Kernel)** addresses the **structural complexity** and **learnability** of agentic systems. By shifting the focus from "Prompt Engineering" to **"Agent Engineering"**, SPAK provides a framework where agents are built as verifiable, formal artifacts.

**Key Contributions:**
1.  **Formal-Spec Driven Synthesis:** A neuro-symbolic approach where Large Language Models (LLMs) are constrained by **Semantic IR (AISpec)**.
2.  **Category Theory Foundation:** Agents are formalized as **Endofunctors on Semantic Categories**, providing a rigorous mathematical backbone for agent behavior.
3.  **Educational Path (Agent Maturity Levels):** A curriculum-based approach that allows developers to learn agent construction by gradually increasing specification complexity (from Level 0 to Level 5).
4.  **Algebraic Effect Runtime:** Separation of **Policy** (LLM decision) and **Runtime** (side effects), ensuring safety and observability.

---

## 2. Formal Semantics: Agent as Endofunctor

SPAK reframes agent execution as a trajectory through a **Semantic State Space**.

*   **Semantic Category ($\\mathcal{C}$):** Defined by the `system` and its `state` objects.
*   **Morphism ($f: S \to S'$):** Defined by `function` blocks, representing pure semantic transitions.
*   **Endofunctor ($F: \\mathcal{C} \to \\mathcal{C}$):** The agent itself, which iteratively applies morphisms to transform its internal state.
*   **Algebraic Effects:** Managed interactions with the external world (LLM, IO), yielding "requests" to the Kernel rather than direct mutations.

---

## 3. The Agent Maturity Framework (Evaluation)

To evaluate the efficacy of the spec-driven approach, we propose an **Agent Curriculum** based on maturity levels. This serves as our primary qualitative and quantitative benchmark.

| Level | Name | Semantic Construct | SPAK Implementation Status |
| :--- | :--- | :--- | :--- |
| **0** | **Static Responder** | `function` (Input $\\to$ Output) | ✅ **Completed** |
| **1** | **Context-Aware Bot** | `state` (History/Memory) | ✅ **Completed** |
| **2** | **Tool-Use Agent** | `effect` (External API/REPL) | 🚧 In Progress |
| **3** | **Planning Agent** | `workflow` (Loop/Condition) | 📅 Planned |
| **4** | **Multi-Agent System**| `composition` (Shared Space) | 📅 Planned |
| **5** | **Self-Improving** | `meta-build` (Self-Recursion) | 📅 Planned |

### Preliminary Results (Level 0-1)
We successfully demonstrated that the SPAK **Builder** can synthesize Python code from a minimal `AgentSpec` for Level 0 and 1. The **Verifier** successfully caught argument mismatches in generated tests, triggering a **Self-Repair** cycle that converged on a correct implementation.

---

## 4. Analysis of Prior Art (Refined)

### A. Process-Oriented vs. Kernel-Oriented
*   **MetaGPT/ChatDev:** Focus on human-like social orchestration (SOPs).
*   **SPAK:** Focus on **Machine-Verifiable Constraints**. We define the *Kernel* (OS) first, then the *Agent* (Process).

### B. Unit Testing vs. Formal Invariants
*   **Reflexion:** Uses unit tests for feedback.
*   **SPAK:** Uses **Hoare-logic style invariants** and **Semantic IR matching** in addition to unit tests, ensuring structural integrity before execution.

---

## 5. Positioning & Target Venues

**Proposed Title:**
> **"SPAK: A Formally Verified, Spec-Driven Kernel for Curriculum-Based AI Agent Synthesis"**

**Target Venues:**
*   **KAIS** (Knowledge-Based Systems)
*   **ICSE** (International Conference on Software Engineering - SE Education track)
*   **ASE** (Automated Software Engineering)

---

## 6. Appendix: AgentSpec Grammar v0.4

```ebnf
AgentSpec ::= MetaDef SystemDef
SystemDef ::= "system" Name "{" ComponentDef* "}"
ComponentDef ::= "component" Name "{" MemberDef* "}"
MemberDef ::= "state" Name "{" Field* "}"
            | "function" Name "(" Params ")" "->" Type "{" Body "}"
            | "invariant" StringLiteral
```

