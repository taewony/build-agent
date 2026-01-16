아래는 **AgentSpec v0.4 형식**에 맞춰 작성한
**Growth Mindset Coaching Agent**의 완성도 높은 예시입니다.

* **논문 Appendix / POC / 학생 교육용**으로 바로 사용 가능
* 각 블록마다 **“왜 이게 필요한지”가 드러나도록 주석(comment)**을 충분히 추가
* *prompt*가 아니라 **의미 구조(spec)** 를 설계하고 있다는 점이 분명히 보이도록 구성

---

```agentspec
////////////////////////////////////////////////////////////
// AgentSpec v0.4
// Growth Mindset Coaching Agent
//
// This agent is designed to support continuous personal growth
// by operating over a structured semantic state rather than
// producing isolated answers.
//
// Core idea:
//   - Coaching is a semantic state transition process
//   - The agent preserves intent (growth) across transformations
//   - LLMs are used only as proposal generators, never as authority
////////////////////////////////////////////////////////////

meta {
  name        = "GrowthMindsetCoach"
  version     = "0.4"
  description = "A growth-centric personal coaching agent based on semantic state transitions"
  authors     = ["Anonymous"]
  license     = "Research"
}

////////////////////////////////////////////////////////////
// A. Semantic Category
//
// This explicitly defines the semantic space in which the agent
// operates. All agent behavior must stay inside this category.
//
// Objects   : GrowthState
// Morphisms : Meaning-preserving coaching transformations
////////////////////////////////////////////////////////////

semantic_category GrowthCategory {
  object GrowthState

  // Core meaning transformations in growth coaching
  morphism ReflectExperience
  morphism ReframePerspective
  morphism PlanNextAction
}

////////////////////////////////////////////////////////////
// B. Algebraic Effects
//
// Effects define *what kinds of interactions are allowed*.
// They do NOT define how those interactions are executed.
//
// The kernel mediates all effects.
////////////////////////////////////////////////////////////

effect LLM {
  // LLM is treated as a non-deterministic proposal generator.
  // It never mutates state directly.
  operation generate(prompt: Prompt)
    -> Result<LLMProposal, LLMError>
}

effect Memory {
  // Optional long-term memory (journals, past sessions)
  operation load(key: String)
    -> Result<Value, Error>

  operation store(key: String, value: Value)
    -> Result<Unit, Error>
}

////////////////////////////////////////////////////////////
// C. Algebraic Data Types (Semantic Domain Modeling)
//
// These types define the *meaningful vocabulary* of growth coaching.
// They are immutable and serializable.
////////////////////////////////////////////////////////////

type Goal =
  | Undefined
  | Defined(description: String)

type Experience =
  | Event(description: String)
  | Feeling(description: String)

type Reflection =
  | Insight(text: String)
  | Reframe(text: String)

type Action =
  | SmallStep(description: String)
  | Experiment(description: String)

type Signal =
  | Low
  | Medium
  | High

////////////////////////////////////////////////////////////
// D. Semantic State
//
// This is the persistent meaning state of the coaching process.
// The agent never "answers questions"; it evolves this state.
////////////////////////////////////////////////////////////

state GrowthState {

  // The user's current growth goal (may evolve slowly)
  goal : Goal

  // Raw experiences reported by the user
  experiences : List<Experience>

  // Interpreted meaning derived from experiences
  reflections : List<Reflection>

  // Concrete next actions (must be actionable)
  next_actions : List<Action>

  // Rough motivational signal used for pacing
  motivation_level : Signal

  // Accumulated semantic context (conversation, notes, history)
  context : Context
}

////////////////////////////////////////////////////////////
// E. Context as a Monoidal Structure
//
// Context is composable, associative, and has an identity.
// This allows selective injection, replay, and partial execution.
////////////////////////////////////////////////////////////

context_monoid {
  identity: EmptyContext
  compose: SemanticMerge
}

////////////////////////////////////////////////////////////
// F. Invariants (Intent & Meaning Preservation)
//
// Invariants encode the coaching philosophy.
// Violating an invariant is a semantic failure.
////////////////////////////////////////////////////////////

invariant PreserveGrowthIntent:
  forall s, s':
    ReflectExperience(s) == s' implies s.goal == s'.goal

invariant NoJudgementLanguage:
  not contains_judgemental_language(s.reflections)

invariant Actionability:
  s.next_actions.size > 0 implies
    forall a in s.next_actions: is_small_and_concrete(a)

////////////////////////////////////////////////////////////
// G. Morphisms (Semantic Transitions)
//
// Each morphism represents a meaning-preserving transformation.
// Effects are explicitly declared.
////////////////////////////////////////////////////////////

morphism ReflectExperience
  : GrowthState -> GrowthState
effects { LLM }
ensures { PreserveGrowthIntent }

////////////////////////////////////////////////////////////
// Turns raw experiences into neutral insights.
// Does NOT evaluate success or failure.
////////////////////////////////////////////////////////////

morphism ReframePerspective
  : GrowthState -> GrowthState
effects { LLM }
ensures { NoJudgementLanguage }

////////////////////////////////////////////////////////////
// Shifts interpretation without changing facts.
// Focuses on learning and possibility.
////////////////////////////////////////////////////////////

morphism PlanNextAction
  : GrowthState -> GrowthState
effects { LLM }
ensures { Actionability }

////////////////////////////////////////////////////////////
// Produces at least one small, concrete next step.
////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////
// H. Semantic Functors
//
// These define structure-preserving projections from
// semantic meaning to external representations.
////////////////////////////////////////////////////////////

functor ToDocs
  : GrowthCategory -> DocumentCategory

functor ToCode
  : GrowthCategory -> CodeCategory

////////////////////////////////////////////////////////////
// I. Natural Transformations (Plan Refinement)
//
// Used when moving from coarse coaching plans
// to more concrete, operational ones.
////////////////////////////////////////////////////////////

natural_transform RefineCoachingPlan
  : ToDocs_coarse => ToDocs_refined

////////////////////////////////////////////////////////////
// J. Agent as Endofunctor
//
// The agent itself is defined as an endofunctor
// repeatedly applied to the semantic state.
////////////////////////////////////////////////////////////

agentfunctor GrowthCoachingLoop
  : GrowthCategory -> GrowthCategory {

  apply {
    ReflectExperience
    ReframePerspective
    PlanNextAction
  }

}

////////////////////////////////////////////////////////////
// K. Workflow (Readable Macro Structure)
//
// This is syntactic sugar over the functor application.
// It exists for readability and teaching.
////////////////////////////////////////////////////////////

workflow CoachingSession {
  step ReflectExperience
  step ReframePerspective
  step PlanNextAction
}

////////////////////////////////////////////////////////////
// L. Tests (Semantic Verification)
//
// Tests assert semantic properties, not surface text.
////////////////////////////////////////////////////////////

test "Every coaching session yields an actionable step" {
  given initial_state
  when GrowthCoachingLoop applied
  then state.next_actions.size >= 1
}

test "Goal is preserved during reflection" {
  given state with goal Defined("Improve focus")
  when ReflectExperience
  then state.goal == Defined("Improve focus")
}

////////////////////////////////////////////////////////////
// End of AgentSpec
////////////////////////////////////////////////////////////
```

---

## 이 AgentSpec이 잘 설계되었다고 말할 수 있는 이유

### 1. **Prompt가 아니라 의미 구조를 정의**

* “무엇을 말할까?” ❌
* “어떤 의미 상태를 어떻게 변화시킬까?” ✅

### 2. **Growth mindset의 철학이 invariant로 고정**

* 평가 없음
* 목표 존중
* 작은 실행

### 3. **LLM은 항상 통제된 위치**

* morphism 내부
* effect로만 사용
* kernel이 승인·거부·재생 가능

### 4. **Agent 생성이 쉬움**

* 다른 coaching agent는:

  * `state`
  * `invariants`
  * `morphisms`
    만 바꾸면 됨