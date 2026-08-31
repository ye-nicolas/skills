---
name: behavior-outcome-analysis
description: Analyze requirements, source code, tests, configuration, API contracts, schemas, fixtures, and data states to derive all meaningful system outcomes and test scenarios, including non-success responses, exceptions, state changes, side effects, retries, and unverified behavior. Use when the user asks what a code path can return or how it behaves beyond HTTP 200. Do not conduct a requirements interview or implement tests.
---

# Behavior Outcome Analysis

Derive what the system can actually do from its requirements, implementation, tests, configuration, and data conditions. Produce an evidence-backed behavior matrix and test-scenario list. Analyze outcomes; do not fix code, write tests, or conduct a user interview.

## Scope boundary

This skill answers: “Given these requirements, code paths, and data states, what can happen?”

- Use `$requirements-interview` when the main task is to question the user and clarify product intent.
- Use `$markdown-docs` when the main task is to document existing code.
- Use `$java-junit`, `$springboot-testing`, `$springboot-tdd`, or
  `$java-verification` after this analysis when implementing or running tests.
- Do not silently fill missing requirements with framework conventions. Record unknowns and return targeted questions for a later requirements interview.

## Evidence sources

Inspect the smallest complete set of relevant evidence:

- Requirements, user stories, acceptance criteria, API specifications, and existing documentation.
- Entry points, controllers, handlers, services, repositories, clients, serializers, exception handlers, and state transitions.
- Tests, fixtures, mocks, seed data, migrations, database constraints, schemas, and sample payloads.
- Configuration, feature flags, environment variables, dependency versions, and deployment assumptions.

Label each claim as one of:

- `required`: explicitly stated by a requirement or contract.
- `observed`: directly shown by implementation, configuration, data, or test evidence.
- `inferred`: derived from a connected code path but not directly asserted.
- `missing`: required or expected but not implemented or covered.
- `contradictory`: requirements, code, tests, or data disagree.
- `unknown`: cannot be determined without more evidence or a decision.

## Analysis workflow

1. Define the target flow, public entry point, scope, and available artifacts. Do not analyze the entire repository when one endpoint, command, job, or service is in scope.
2. Build an evidence map: symbol or requirement, source location, relevant condition, data assumption, and confidence label.
3. Trace the normal path end to end. Follow input binding, validation, branching, external calls, persistence, transaction boundaries, exception mapping, serialization, and side effects.
4. Enumerate scenario dimensions before writing outcomes:
   - input: valid, invalid, missing, null, empty, malformed, oversized, duplicate, and boundary values;
   - identity: unauthenticated, unauthorized, wrong tenant, expired credential, and permitted actor;
   - state: record exists, missing, stale, already processed, conflicting, partially initialized, and corrupted;
   - dependency: success, empty, malformed, rejected, timeout, connection failure, rate limit, retry, and recovery;
   - execution: concurrency, ordering, cancellation, transaction failure, restart, clock/time zone, and feature flag;
   - data shape: cardinality, enum values, null semantics, precision, units, encoding, and referential constraints.
5. Trace each meaningful combination only as far as it changes behavior. Avoid a combinatorial explosion; explain which combinations were grouped and why.
6. Record every materially different outcome, not only successful responses. Include response status and body, exception, persisted state, rollback, emitted event, cache/file/message side effect, retry behavior, and observable logging or metrics when supported by evidence.
7. Compare required, observed, and inferred behavior. Highlight missing, contradictory, and unknown outcomes. Never call a path “covered” merely because a nearby happy-path test exists.
8. Rank scenarios by impact, likelihood, and uncertainty. Recommend the smallest test type that can prove each high-risk behavior.

## Outcome matrix

Use a table like this as the primary artifact:

| ID | Scenario / input / state | Evidence and code path | Actual or possible outcome | Required outcome | Side effects / state | Coverage and gap |
|---|---|---|---|---|---|---|
| O-01 | Record missing | repository returns empty; handler maps exception | `404` with error body | `404` | no write | integration test missing |
| O-02 | Duplicate create | unique constraint throws; transaction boundary rolls back | `409` or unhandled `500` | `409` | no committed row | requirement/code mismatch |
| O-03 | Downstream timeout | client timeout, retry exhausted | `504`, propagated error, or fallback | unknown | event not published | confirm contract |

For each row, answer:

1. What inputs and preconditions trigger it?
2. Which branch, exception, or external result produces it?
3. What does the caller observe?
4. What data and side effects remain after it?
5. Is it required, implemented, tested, or unknown?

## Outcome categories

Check the categories relevant to the target flow:

- Success variants: different `2xx` statuses, response shapes, empty success, partial result, pagination, and idempotent repeat.
- Input and contract failures: binding, validation, malformed JSON, missing field, unsupported enum, size limit, and content negotiation.
- Identity and access: `401`, `403`, tenant mismatch, filtered data, and audit behavior.
- Resource state: missing, duplicate, stale version, already completed, soft-deleted, and conflicting resource (`404`, `409`, or domain error).
- Dependency and infrastructure: timeout, retry exhaustion, circuit breaker, rate limit, malformed downstream data, unavailable database, and serialization failure.
- Persistence and consistency: commit, rollback, constraint violation, optimistic lock, partial write, duplicate event, cache invalidation, and transaction/event ordering.
- Concurrency and lifecycle: race, ordering, cancellation, restart, repeated delivery, scheduler overlap, and resource cleanup.
- Security and privacy: data leakage through errors or logs, over-broad access, injection boundary, secret exposure, and audit gaps.
- Reactive behavior: `Mono.empty`, `Mono.error`, cancellation, backpressure, timeout, retry, dropped signal, and blocking boundary.

## Java and Spring analysis

For Java and Spring, inspect the actual `@ControllerAdvice`, validation annotations, `ResponseEntity`, Jackson configuration, transaction annotations, repository behavior, database constraints, event listeners, cache annotations, and security configuration. Do not infer status codes solely from the controller signature.

For Spring MVC, include blocking calls, transaction rollback, async executor behavior, and thread-safety assumptions. For Spring WebFlux, include publisher cardinality, subscription, cancellation, scheduler changes, backpressure, timeout, retry, and blocking calls accidentally placed on the event loop. Use `$springboot-reactive-patterns` for reactive design details.

For persistence, distinguish:

- application-level validation from database constraints;
- a missing record from an empty query result;
- a transaction that has rolled back from one that has not yet committed;
- a published event from an event that is only scheduled or attempted.

## Test scenario recommendations

Map each high-risk outcome to a verification level without implementing it:

| Outcome type | Smallest useful verification |
|---|---|
| Pure branch or mapping | unit test |
| Controller status/body/validation | MVC or WebFlux HTTP test |
| Repository, transaction, constraint, or serialization | integration test |
| External client contract and retry | contract or focused integration test |
| Event, cache, queue, or side effect | integration test with observable boundary |
| Concurrency, timeout, backpressure, or cancellation | deterministic scheduler/concurrency test |
| End-to-end permission or tenant flow | API/system test |

Include scenario priority and the reason it matters. Prefer a few high-value cases that distinguish outcomes over a large list of equivalent successful inputs.

## Output format

Return:

1. **Scope and evidence** — analyzed entry point, artifacts, and limits.
2. **Behavior summary** — normal flow and important branches.
3. **Outcome matrix** — all materially different results, including non-200 results and side effects.
4. **Requirement versus implementation gaps** — missing, contradictory, or unverified behavior.
5. **Risk-ranked test scenarios** — scenario, expected/observed result, verification level, and priority.
6. **Targeted questions** — only questions that require the product owner or developer to decide; hand these to `$requirements-interview` when an interactive interview is desired.

## Quality gate

Before finishing, confirm:

- The analysis used requirements, code, tests, configuration, and data evidence that was actually available.
- Non-success results, exceptions, empty results, state changes, and side effects were considered.
- Every important outcome distinguishes expected, observed, tested, and unknown behavior.
- Status codes and error bodies come from code or contract evidence, not assumptions.
- Data constraints, null semantics, duplicate behavior, transaction boundaries, and dependency failures were considered where relevant.
- The output recommends verification levels but does not modify code or pretend tests passed.
