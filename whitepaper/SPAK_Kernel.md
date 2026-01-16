# SPAK Kernel Specification

This document merges and refines the concepts from previous AgentSpec versions into a cohesive Kernel Specification.

## 1. Introduction

The **Spec-Driven Programmable Agent Kernel (SPAK)** is a runtime environment designed to execute agents defined by **AgentSpec**. It acts as an operating system for agents, providing resource management, isolation, and verification.

## 2. Kernel Architecture

The kernel is composed of the following core components:

### 2.1 Compiler
*   **Role:** Parses AgentSpec DSL into Semantic IR.
*   **Input:** `.md` spec files.
*   **Output:** AST (Abstract Syntax Tree) / Semantic IR.

### 2.2 Verifier
*   **Role:** Enforces structural and behavioral correctness.
*   **Checks:**
    *   **Static:** Type checking, invariant consistency.
    *   **Dynamic:** Runtime behavior against test vectors.

### 2.3 Runtime
*   **Role:** The execution engine for agents.
*   **Mechanism:** Algebraic Effect handling.
*   **Responsibility:**
    *   Intercepts `perform` calls.
    *   Routes effects to appropriate handlers (LLM, FileSystem, Memory).
    *   Logs execution traces.

### 2.4 Builder (Meta-Agent)
*   **Role:** The "Auto-Coder" component.
*   **Function:** Uses an LLM to synthesize Python implementation code from the Semantic IR.
*   **Recursion:** The Builder is itself an agent running on the Kernel.

## 3. The Recursive Loop

The defining feature of SPAK is its recursive nature:
1.  **Spec:** `SPEC.spak.md` defines the Kernel.
2.  **Build:** The Kernel uses the Builder to implement `SPEC.spak.md`.
3.  **Run:** The resulting code *is* the new version of the Kernel.

## 4. Formal Verification

SPAK aims to provide formal guarantees:
*   **Effect Safety:** No side effect occurs without Kernel mediation.
*   **State Integrity:** State transitions only happen via defined Morphisms.

## 5. Roadmap

*   **v0.4 (Current):** Basic Kernel, Compiler, and Builder.
*   **v0.5:** Enhanced Type System, Hierarchical Memory.
*   **v1.0:** Self-Hosting (The "Singularity" Step).
