---
name: java-implementation-planning
description: Create repository-evidence-based implementation plans for approved or sufficiently clear Java and Spring changes. Use when the user wants an ordered, file-level plan before coding for a feature, bug fix, refactor, migration, or dependency change. Do not conduct a requirements interview, make unresolved product decisions, or implement the plan.
---

# Java Implementation Planning

Turn a clear change contract into an implementation plan that another engineer
or agent can execute without rediscovering the repository. Plans must preserve
known behavior, expose material decisions, and attach verification to every
functional slice. Do not write production code while planning.

## Establish planning readiness

Inspect repository instructions, build files, the public entry point, important
callers, tests, configuration, schemas, migrations, and the specialist boundary
that owns the change. Record the requested outcome, explicit non-goals, current
behavior, intended behavior, compatibility constraints, and available evidence.

Proceed when the requirement is approved or sufficiently clear for the next
implementation decision. If a missing product, ownership, security, data, or
compatibility decision would materially change the plan, ask one targeted
question or route an explicitly requested discovery session to
`$requirements-interview`. Use `$java-architecture-review` when the unresolved
choice is an architecture boundary rather than a product requirement.

Do not infer a contract from class or method names, treat a proposed API shape
as approved merely because it appears in the request, or invent exact file
paths before inspecting the repository.

## Build the change map

1. Trace the current flow from its public entry point through validation,
   decisions, state changes, external effects, errors, and tests.
2. Identify the smallest coherent behavior change and every directly affected
   caller, contract, data shape, configuration key, and document.
3. State what must remain unchanged, including ordering, failure semantics,
   transactions, idempotency, compatibility, and lifecycle boundaries.
4. Identify dependencies between changes. Separate prerequisites from work that
   can genuinely proceed independently.
5. Use `$behavior-outcome-analysis` first when materially different outcomes or
   side effects remain unknown; carry its evidence into the plan instead of
   repeating the analysis.

## Define functional slices

Make each task an independently reviewable functional slice with one observable
completion boundary. Fold scaffolding, configuration, documentation, and tests
into the slice whose behavior needs them. Split work when a reviewer could
accept one outcome while rejecting another, not to satisfy an arbitrary task
count or time estimate.

For each slice specify:

- objective and externally observable behavior;
- files and symbols to modify, create, or remove, based on inspected evidence;
- contract changes and contracts deliberately preserved;
- ordered implementation steps at the level needed to avoid ambiguity;
- focused tests, including important failure paths and the intended red signal
  for regression or test-first work;
- exact repository-owned verification command or manual check and its expected
  result;
- dependencies, risk, migration or rollout concerns, and rollback boundary.

Prefer symbols and stable file paths over brittle line numbers. Include small
pseudocode or signatures only when they clarify a non-obvious contract; do not
pre-write the implementation or force a design that should remain local to the
implementer.

## Cross-cutting decisions

Include a cross-cutting item only when repository evidence or the approved
change makes it material:

- public API, serialization, event, schema, or configuration compatibility;
- database migration, backfill, deployment ordering, or rollback;
- authorization, sensitive data, dependency risk, or audit behavior;
- concurrency, retry, cancellation, idempotency, or capacity;
- telemetry needed to validate rollout or diagnose failure; and
- dependency, build, generated-source, or supported-JDK changes.

Do not add a generic security, observability, or documentation phase to every
plan. Route specialist decisions to the corresponding installed skill only when
that boundary affects correctness.

## Review and deliver the plan

Read [the plan template](references/plan-template.md) when producing a durable
plan artifact. Adapt it to the repository instead of retaining empty sections.

Before delivery, confirm that:

- every task maps to the requested outcome and repository evidence;
- task order follows real dependencies and keeps the repository buildable;
- every changed production path has focused behavioral verification;
- failure, migration, rollout, and rollback behavior is explicit where needed;
- assumptions and open decisions are visible and assigned a validation action;
- no unrelated cleanup, speculative abstraction, or unapproved dependency is
  included; and
- the plan ends at verified implementation, not merely written code.

Report the evidence inspected, the ordered slices, unresolved blockers, and the
recommended first slice. Wait for implementation authorization when the user
asked only for a plan.
