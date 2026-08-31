---
name: java-architecture-review
description: Review Java or Spring architecture using repository evidence to assess module boundaries, dependency direction, ownership, coupling, runtime interactions, and changeability. Use for architecture reviews, modularization, package or service boundaries, dependency cycles, or cross-cutting structural refactors; do not use for ordinary local code cleanup.
---

# Java Architecture Review

Evaluate whether the system's boundaries make its responsibilities, state,
dependencies, and operational behavior understandable and safely changeable.
Recommend the smallest structural correction supported by current requirements;
do not impose a fashionable architecture or redesign the whole repository.

## Establish the architecture in use

Inspect before judging:

- repository and directory instructions, build modules, source sets, and JDK;
- public entry points, package and module dependencies, and important callers;
- domain ownership, persistence and transaction boundaries, external clients,
  messages, caches, background work, and configuration;
- runtime and deployment units, data ownership, scaling assumptions, and
  failure isolation; and
- architecture tests, ADRs, diagrams, conventions, and recent relevant changes.

Treat diagrams and naming as claims. Confirm the effective dependency and
runtime paths in code and configuration.

## Set the evidence boundary

- Before calling a problem a current high-impact defect, prove an active entry
  point or caller, the relevant input or state, the runtime path, and the
  resulting side effect or failure. A Spring stereotype, suspicious method, or
  static search result establishes a candidate, not reachability.
- Treat commented mappings, inactive profiles, unused beans, and legacy
  implementations without an active caller as conditional or legacy risks.
  State the activation condition instead of describing them as live defects.
- When exposure depends on a gateway, deployment policy, or other evidence not
  present in the repository, report what the code permits and make the missing
  external condition explicit.

## Review dimensions

### Cohesion and ownership

- Each module or component should have one explainable responsibility and own
  the invariants, state, and lifecycle needed to fulfil it.
- Keep business rules with the domain or application boundary that owns them;
  avoid shared utility modules that become unowned dumping grounds.
- Separate materially different change reasons, but do not split cohesive code
  merely to create more layers or services.

### Dependency direction and contracts

- Trace compile-time and runtime dependencies separately. Identify cycles,
  backdoors, reflection, generated wiring, and shared database coupling that a
  package diagram may hide.
- Dependencies should point toward stable, meaningful contracts. Introduce an
  interface or port only for a real boundary or substitutable role.
- Treat public Java APIs, REST/message schemas, database representation, and
  configuration keys as compatibility surfaces.

### State, consistency, and failure

- Make the owner of each write, transaction, cache, event, retry, lock, and
  background task explicit.
- Identify cross-boundary workflows whose partial failure, ordering,
  idempotency, or recovery behavior is hidden.
- Do not recommend service extraction without a credible data ownership,
  deployment, observability, and operational model.

### Changeability and operations

- Compare the proposed boundary with actual team and deployment constraints.
- Prefer a modular monolith when independent deployment and data ownership are
  not demonstrated needs; prefer independent services only when their benefits
  justify distributed failure modes.
- Check whether logs, metrics, traces, health signals, and rollout boundaries
  follow the same ownership model as the code.

## Preserve concrete contract coverage

After mapping the architecture, inspect representative active high-risk paths
for concrete contract failures that can be obscured by structural analysis:

- dynamic query or command construction and untrusted boundary inputs;
- validation that occurs after dereference, indexing, or side effects;
- swallowed exceptions and ambiguous `null`, `false`, or success outcomes;
- ownership and lifecycle of mutable singleton state, executors, resources,
  transactions, and asynchronous work;
- sensitive-data logging and external side effects that occur before commit;
  and
- message acknowledgement, retry, idempotency, ordering, and send-result
  handling when messaging is present.

Keep this sweep risk-driven rather than exhaustive style lint. Report a local
code issue in an architecture review when its consequence crosses an ownership,
consistency, security, lifecycle, or failure boundary. Treat broad scans and
counts as candidate discovery, then confirm representative runtime paths.

When re-running or comparing a review, maintain a coverage ledger for prior
confirmed findings: mark each as still present, resolved, superseded, or not
revalidated. Do not silently drop a valid local finding merely because the new
review found more architectural issues.

Use `$springboot-security`, `$jpa-patterns`, `$effective-java-concurrency`,
`$spring-messaging-patterns`, or `$springboot-reactive-patterns` when one of
those specialist contracts determines correctness.

## Evaluate a proposed change

1. State the problem and the quality attribute being improved: correctness,
   change isolation, deployability, reliability, performance, security, or
   operability.
2. Describe the current boundary and the concrete pressure it fails to handle.
3. Compare the smallest viable options, including keeping the current design.
4. Identify compatibility, migration, sequencing, ownership, and rollback
   consequences.
5. Recommend one option and define incremental checkpoints that keep the system
   buildable and behaviorally compatible.

Use `$requirements-interview` when a high-impact product, ownership, deployment,
or compatibility decision lacks an approved requirement. Use
`$contract-first-refactoring` for the implementation of a semantic API change.

## Deliver the review

Report actionable findings in impact order. For each finding include the
affected modules or path, the observed dependency or ownership problem, the
consequence, and the smallest coherent remedy. For every high-impact finding,
show a compact evidence chain such as `entry point -> input/state -> runtime
call -> side effect/failure`. Prioritize demonstrated security or data exposure,
cross-user correctness, irreversible loss, consistency and recovery, and
availability ahead of maintainability pressure. Separate:

- current defects or violated contracts;
- risks that require a stated trigger or scale condition; and
- optional target-state improvements.

Include a compact current-versus-proposed dependency description when it makes
the recommendation easier to verify. If the present architecture fits the
requirements, say so instead of manufacturing a pattern change.
