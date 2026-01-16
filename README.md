# Meta Build-Agent Kernel (MBAK)
## to specify and build the Build-Agent itself and build other domain agent
**"A Formal Spec-Driven, Recursively Self-Improving Agent Kernel"**

This project implements a **Programmable and Verifiable Agent Kernel**. Unlike traditional agent frameworks that focus on "orchestration" (chaining prompts), this system focuses on **"Correctness & Synthesis"**. It treats Agent Logic as an artifact that must be **compiled from a formal specification (AISpec)**, **verified against test vectors**, and **executed within an effect-isolated runtime**.

## 🏗 Core Definition

> **"It is like Terraform for AI Agents, but instead of cloud infrastructure, it manages Software Logic."**

The system operates on three fundamental pillars:

1.  **Compiler, Not Interpreter:** It "compiles" a **Formal Spec (`SPEC.md`)** into an **Executable Agent (`src/*.py`)** using an LLM as the code generator.
2.  **Effect-Isolated Runtime:** It separates **Policy** (Decision) from **Runtime** (Execution) using **Algebraic Effects**. Agents yield intents; the Kernel handles them.
3.  **Recursive Fractal Design:** The system is capable of building itself. A "Build Agent" can define a sub-spec, spawn a "Sub-Build Agent" to implement it, verify it, and merge it back.

---

## 📚 Terminology & Concepts

### 1. The "Inside vs. Outside" Architecture

This system is designed to bridge the gap between High-Level Intent and Low-Level Execution.

| Realm | **Outside the System** | **Inside the System** |
| :--- | :--- | :--- |
| **Agent** | **The Architect** | **The Contractor** |
| **Intelligence** | Frontier Models (GPT-4o, Claude 3.5) + Humans | Local Models (Llama 3, Gemma 2, Qwen 2.5) |
| **Role** | Define **Specs** and **Constraints**. | Implement Logic, Fix Bugs, Pass Tests. |
| **Artifact** | `SPEC.*.md`, `tests.*.yaml` | `src/*.py`, `build/*.html`, `trace.json` |

---

## 🛠 Usage & Workflow

The system runs a **REPL-driven Build Loop**:

```bash
# Start the Kernel Shell (Main Entry Point)
$ python spak.py

# 1. Load a Specification (The Blueprint)
(kernel) > load specs/SPEC.spak.md
[Kernel] Loaded System: SPAK_Kernel

# 2. Verify Structural Integrity
(kernel) > verify kernel
[Static Analysis] Starting verification for system: SPAK_Kernel
...
[Result] Verification PASSED.

# 3. Auto-Implement (The Build)
(kernel) > build
[Builder] Generating code for 'Header' using Local LLM... Done.

# 4. Verify Behavior (The Test)
(kernel) > verify behavior
[Pytest] test_header_rendering ... PASS
```

---

## 🌍 Generic Application Domains

Because the system is "Spec In -> Artifact Out", it can apply to almost anything:

| Domain | Spec (AISpec) | Artifact | Verification |
| :--- | :--- | :--- | :--- |
| **Web Dev** | UI Component / User Flow | HTML / React / Vue | Playwright / Storybook / Lighthouse |
| **Data Eng** | Schema / Pipeline Logic | SQL / Airflow DAGs | Data Quality Tests (GreatExpectations) |
| **DevOps** | Infrastructure State | Terraform / K8s Manifests | terraform plan / Policy-as-Code (OPA) |
| **Research** | Experiment Protocol | Python / Jupyter Notebook | Statistical Significance Check |

### Conclusion: The Build-Agent is generic.

By defining the system as **"Programmable and Verifiable"**, you can use it as a **"Universal Agent Factory"**.

---

## Appendix: Why "Kernel"?

컴퓨터 과학에서 **커널(Kernel)**이라고 부르기 위해서는 자원 관리 및 추상화, 격리 및 보호, 스케줄링 및 제어 기능을 수행해야 합니다.

1.  **자원 관리 (LLM as Resource):** 에이전트는 직접 LLM을 호출하지 않고 커널에 요청합니다.
2.  **격리 및 보호 (Isolation):** 에이전트의 논리와 실제 시스템 실행을 분리하여 안전을 보장합니다.
3.  **제어 (Algebraic Effects):** `perform(WriteFile)` 같은 시스템 콜(Syscall) 인터페이스를 제공합니다.

우리는 에이전트를 위한 운영체제(OS)의 핵심부를 구축하고 있습니다.
