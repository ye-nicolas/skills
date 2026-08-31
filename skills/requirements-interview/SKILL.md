---
name: requirements-interview
description: Conduct a Socratic, one-question-at-a-time interview that turns a rough product or engineering idea into an approved, actionable development specification. Use when the user has a feature request, refactor, workflow, API, or Java/Spring change and wants probing questions, assumption testing, alternatives, acceptance criteria, and a Markdown spec. Do not use for documenting existing code; use $markdown-docs.
---

# Requirements Interview

Turn an incomplete idea into a development-ready specification through a respectful but persistent interview. Ask until the problem, scope, behavior, constraints, risks, and acceptance criteria are clear enough for implementation. Do not rush to code or treat an attractive idea as a validated requirement.

## Non-negotiable behavior

- Read the available project context before asking discovery questions: repository instructions, existing docs, relevant source, tests, configuration, recent changes, and the current conversation. Never ask for information that is already available.
- Ask exactly one meaningful question per turn by default. Briefly reflect the user's last answer, state the remaining uncertainty, and ask the next highest-value question.
- Keep interviewing until the user says to stop, the readiness gate passes, or a blocking unknown has been explicitly recorded as requiring research or a decision.
- Challenge assumptions with concrete counterexamples, edge cases, and trade-offs. Be direct and respectful; the goal is to improve the idea, not to win an argument.
- Separate facts, user wishes, assumptions, decisions, proposals, and open questions. Never present an unconfirmed idea as current system behavior.
- Do not implement code, modify production behavior, or invoke implementation skills during the interview. Produce the specification first and wait for approval.

## Interview state

Maintain a compact working ledger in the conversation:

```text
Problem: what pain or opportunity exists
Users: who experiences it and who operates it
Desired outcome: measurable change
Scope: included and explicitly excluded behavior
Known facts: evidence from the user or repository
Assumptions: statements awaiting confirmation
Decisions: choices the user has accepted
Open questions: unresolved items, ranked by risk
Acceptance criteria: observable conditions of satisfaction
```

Update the ledger after each answer. Do not repeatedly restart the interview or dump the entire ledger after every turn; summarize only the changes and the next decision needed.

## Phase 1: Establish context

1. Identify the target product, service, module, repository, or workflow from the conversation and local project context.
2. Inspect relevant files before asking questions when a repository is available. Check existing architecture, entry points, tests, configuration, API contracts, persistence, and documentation conventions.
3. Identify what is already known and what remains uncertain. Make the first question demonstrate awareness of the available context.
4. If no implementation context exists, ask for the smallest missing context needed to scope the idea, not a generic questionnaire.

## Phase 2: Conduct the interview

Choose the next question based on risk and dependency, not a rigid script. Use this order as a guide:

1. **Problem and outcome** — What problem is being solved, for whom, and what observable result would make it worthwhile?
2. **Current behavior** — How is the task done today, what fails, and what workaround exists?
3. **Users and scenarios** — Who initiates the flow, who is affected, and what are the primary and exceptional journeys?
4. **Scope** — What must be included, what is explicitly out of scope, and what tempting adjacent work should not be added?
5. **Behavior and contracts** — What inputs, outputs, state transitions, permissions, API shapes, or user-visible messages are required?
6. **Data and dependencies** — What data is created or changed, who owns it, what systems are integrated, and what consistency or transaction rules apply?
7. **Constraints** — What compatibility, platform, deadline, budget, team, library, deployment, or regulatory constraints limit the design?
8. **Failure and edge cases** — What happens on invalid input, duplicates, retries, partial failure, timeout, cancellation, concurrent access, missing data, or downstream outage?
9. **Security and privacy** — Who may perform each action, what data is sensitive, and what must be audited, masked, encrypted, or rate-limited?
10. **Performance and scale** — What latency, throughput, volume, concurrency, availability, or resource limits matter? Which numbers are required versus merely preferred?
11. **Operations** — How will success, failure, saturation, and rollout be observed? What logs, metrics, traces, alerts, feature flags, migration, and rollback are needed?
12. **Validation** — What examples, tests, acceptance criteria, or user checks prove the outcome is achieved?

Skip irrelevant categories, but do not skip them silently when they could change the design. Ask for a concrete example whenever an answer is abstract. Ask for a counterexample whenever a rule sounds absolute.

## Question techniques

Use questions that expose assumptions:

- “What should happen if this is called twice or arrives out of order?”
- “Which part is required for the first usable version, and which part is a later enhancement?”
- “What would convince you this succeeded in production?”
- “What is the most expensive or dangerous failure we need to prevent?”
- “If we remove this constraint, what simpler design becomes possible?”
- “Is this a requirement, an implementation preference, or an assumption?”

When the user gives an ambiguous answer:

1. Reflect the interpretation in one sentence.
2. Give a small concrete example or two plausible interpretations.
3. Ask one question that selects between them.

When the user does not know:

- Record the unknown instead of fabricating an answer.
- Explain why it matters and suggest the smallest validation or experiment.
- Continue with non-blocking questions; pause before making a decision that depends on it.

When alternatives matter, first understand the goal and constraints, then present two or three viable approaches with trade-offs. Recommend one, but ask the user to choose or approve it. Do not hide a major architectural choice inside prose.

## Java and Spring prompts

For Java or Spring ideas, explicitly probe the dimensions that commonly change implementation:

- Spring MVC versus WebFlux and whether the request path is blocking or non-blocking.
- Public REST or messaging contracts, status codes, validation, idempotency, pagination, and compatibility.
- Domain ownership, persistence model, JPA/JDBC versus R2DBC/reactive data access, transaction boundaries, and migrations.
- Authentication, authorization, tenant isolation, sensitive data, audit requirements, and dependency boundaries.
- Concurrency, ordering, retry, timeout, backpressure, cancellation, scheduling, and executor ownership.
- Test strategy, observability, deployment topology, feature flags, rollback, and operational runbooks.

Use `$springboot-patterns`, `$springboot-reactive-patterns`, `$springboot-security`, `$jpa-patterns`, `$effective-java-concurrency`, or `$springboot-tdd` only after the interview identifies the relevant implementation domain. They are companion implementation/review skills, not substitutes for resolving the product intent.

## Readiness gate

Do not declare the idea ready until the following are answered or explicitly marked as accepted unknowns:

- Problem, users, desired outcome, and success measure.
- Primary scenarios, important alternate paths, and explicit non-goals.
- Functional behavior and externally visible contracts.
- Data ownership, dependencies, permissions, and lifecycle.
- Failure modes, edge cases, security, privacy, and operational expectations.
- Performance or scale targets where they affect design.
- Testable acceptance criteria and validation plan.
- Chosen approach, rejected alternatives, risks, rollout, and rollback.

If a missing answer is high-risk, keep interviewing. If it is low-risk, record it under `Open questions` with an owner or validation action when known.

## Spec approval workflow

1. Present the proposed design in short sections: problem, goals, non-goals, behavior, design, risks, and acceptance criteria.
2. Ask for approval or corrections. Do not write the final spec file until the user approves the design, unless the user explicitly requests a draft.
3. Write the approved document to the user-specified path. If none is given, use `docs/specs/YYYY-MM-DD-<slug>.md` when the repository has a `docs/` convention; otherwise ask before creating a new path.
4. Mark the document status as `Draft`, `Proposed`, or `Approved`. Preserve unresolved items in `Open questions`; do not silently resolve them.
5. Perform a spec self-review for contradictions, vague requirements, missing failure behavior, untestable acceptance criteria, unsupported assumptions, and scope creep.
6. Present the file and a short list of remaining decisions. Wait for the user's final review before starting implementation.

## Development specification structure

Use only sections relevant to the idea, but prefer this structure:

```markdown
# Feature or system name

- Status: Draft | Proposed | Approved
- Owner: known owner or TBD
- Last updated: YYYY-MM-DD

## Summary
## Problem and context
## Goals
## Non-goals
## Users and scenarios
## Requirements
## Proposed design
## API, events, or user-visible contracts
## Data and state changes
## Security and privacy
## Failure modes and operational behavior
## Testing and acceptance criteria
## Rollout and rollback
## Alternatives and trade-offs
## Assumptions and open questions
```

## Completion checklist

- The interview asked one question at a time and did not repeat known information.
- The user's idea was challenged with concrete scenarios, counterexamples, and trade-offs.
- The specification distinguishes current facts from proposed behavior.
- Scope, contracts, edge cases, security, operations, and acceptance criteria are explicit.
- The user approved the design before the final spec was written, unless a draft was explicitly requested.
- The Markdown file is concise, actionable, internally consistent, and ready for implementation planning.

## Pattern references

- Superpowers brainstorming: https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md
- Interview skill example: https://gist.github.com/o-az/b55cc44e01843edd81ccd548d3967a38
