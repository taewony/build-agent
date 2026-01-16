# Appendix A. AgentSpec: A Semantic DSL for Programmable Agents

## A.1 Overview

**AgentSpec** is a domain-specific language (DSL) for specifying **semantic agents as compilable, verifiable, and replayable computational artifacts**.
It reframes LLM-based agents not as probabilistic prompt pipelines, but as **meaning-preserving computational systems** formally defined by:

1.  **Semantic Categories** (State Spaces)
2.  **Morphisms** (Transformations)
3.  **Algebraic Effects** (Side-Effect Management)
4.  **Invariants** (Constraints)

AgentSpec unifies **semantic modeling** with **execution control**, allowing agents to be **compiled** from a formal specification into an executable kernel that enforces safety and correctness.

---

## A.2 Conceptual Foundations

AgentSpec is grounded in a rigorous formal view where an agent is an **Endofunctor on a Semantic Category**.

| Formal Concept | AgentSpec Construct | Description |
| :--- | :--- | :--- |
| **Semantic Category** | `system` / `component` | Defines the objects (state) and morphisms (functions) of the agent. |
| **Object** | `state` | The immutable semantic state of the agent at any point in time. |
| **Morphism** | `function` | Pure transformations that map one state to another ($S \to S'$). |
| **Endofunctor** | `agent` / `workflow` | The high-level process that iteratively transforms the state within the category. |
| **Algebraic Effect** | `effect` | Declarative definitions of side-effects (IO, LLM calls) managed by the kernel. |
| **Natural Transformation** | `refinement` (implied) | The process of refining a high-level plan into concrete actions. |

---

## A.3 Top-Level Grammar

The AgentSpec grammar is designed to be readable by both humans (for reasoning) and machines (for compilation).

```ebnf
AgentSpec ::=
              MetaDef
              SystemDef

MetaDef   ::= "meta" "{" MetaField* "}"
SystemDef ::= "system" Name "{" ComponentDef* "}"

ComponentDef ::= "component" Name "{" MemberDef* "}"
               | "effect" Name "{" EffectOp* "}"
               | "workflow" Name "{" Step* "}"
               | "import" Name

MemberDef    ::= "state" Name "{" Field* "}"
               | "function" Name "(" Params ")" "->" Type FuncBody?
               | "invariant" StringLiteral
               | "description" StringLiteral

FuncBody     ::= "{" LogicExpr "}"
```

---

## A.4 Metadata

Metadata provides contextual information for tooling, provenance, and versioning.

```agentspec
meta {
  name        = "GrowthCoach"
  version     = "0.4"
  description = "Growth-centric semantic coaching agent"
  authors     = ["Research Team"]
  license     = "MIT"
}
```

---

## A.5 Semantic Category (System & State)

The `system` block defines the **Semantic Category** in which the agent operates. The `state` defines the **Objects** in this category.

```agentspec
system GrowthCoach {
  
  component Core {
    state GrowthState {
      goal             : String
      reflections      : List<String>
      next_actions     : List<String>
      motivation_level : String  // "Low" | "Medium" | "High"
    }
  }

}
```

> **Formal Note:** The `GrowthState` represents the set of all possible configurations of the agent. Execution is a trajectory through this state space.

---

## A.6 Algebraic Effects (Effect Interfaces)

Effects represent **requests** to the kernel, not direct execution. This separates the **WHAT** (Policy) from the **HOW** (Runtime).

```agentspec
effect LLM {
  operation generate(prompt: String) -> Result<String, Error>
  operation think(context: String) -> Result<Plan, Error>
}

effect Memory {
  operation remember(fact: String) -> Result<Unit, Error>
  operation recall(query: String) -> Result<List<String>, Error>
}
```

**Semantics:**
*   **Pure Logic:** Agent logic yields *Effect Requests*.
*   **Kernel Mediation:** The Kernel intercepts these requests and decides whether to:
    *   **Execute** (call actual LLM/API)
    *   **Mock** (return cached/dummy data for testing)
    *   **Deny** (enforce safety constraints)

---

## A.7 Morphisms (Functions)

Functions are **Semantic Transitions** ($S \to S'$). They are pure by default and perform side effects only via explicit `perform` statements.

```agentspec
function reflect(state: GrowthState) -> GrowthState {
  // Logic expression or prompt template
  insight = perform LLM.generate("Reflect on: " + state.goal)
  
  return {
    ...state,
    reflections: state.reflections + [insight]
  }
}
```

---

## A.8 Invariants (Constraints)

Invariants define the **Semantic Legality** of state transitions. The Kernel verifies these *before* and *after* every transition.

```agentspec
invariant "Reflections must not be empty after a coaching session."
invariant "Motivation level must be a valid enum value."

// Future: Logical Invariants
// invariant forall s, s': reflect(s) == s' implies s.goal == s'.goal
```

---

## A.9 Agent as Endofunctor (Workflows)

Workflows define how the agent iterates over its state, applying morphisms to achieve a goal. This corresponds to the **Endofunctor** concept ($F: \mathcal{C} \to \mathcal{C}$).

```agentspec
workflow CoachingSession(goal: String) {
  
  // Step 1: Initial Reflection
  step reflect
  
  // Step 2: Reframe the problem
  step reframe
  
  // Step 3: Plan concrete actions
  step plan_next_action
  
}
```

> **Verification:** Because workflows are composed of typed morphisms, the compiler can statically verify that the output type of step $N$ matches the input type of step $N+1$.

---

## A.10 Semantic IR & Compilation

AgentSpec compiles to a **Semantic Intermediate Representation (Semantic IR)**, which is then synthesized into executable code (e.g., Python).

1.  **Parsing:** `AgentSpec` $\to$ `AST`
2.  **Analysis:** Type checking and Invariant extraction.
3.  **Synthesis:** `AST` $\to$ `Python (src/*.py)` + `Tests (tests/*.yaml)`

This process ensures that the **Implemented Agent** is mathematically aligned with the **Specified Agent**.

---

## A.11 Kernel Specification (SPAK)

The **Spec-Driven Programmable Agent Kernel (SPAK)** acts as the operating system for these agents.

```kernelspec
kernel SPAK {
  meta {
    version = "0.4"
    role    = "Semantic Agent Kernel"
  }

  // The Kernel itself is defined by components
  component Runtime
  component Verifier
  component Builder
}
```

## A.12 Conclusion

By formalizing agents using **AgentSpec**, we move from "Prompt Engineering" to **"Agent Engineering"**. We gain:

*   **Predictability:** Strict state and type boundaries.
*   **Observability:** Full trace of effect execution.
*   **Reusability:** Modular components and effects.
*   **Safety:** Kernel-enforced invariants and sandboxing.

```