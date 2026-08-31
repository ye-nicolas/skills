---
name: java-engineering-navigator
description: Route Java and Spring software-engineering tasks to the narrowest focused local skill or ordered sequence of skills. Use when a request is broad, ambiguous, or spans requirements, behavior, debugging, architecture, implementation, testing, messaging, persistence, security, concurrency, performance, observability, builds, documentation, or verification. Inspect the task and stack first; do not replace specialist guidance.
---

# Java Engineering Navigator

Select the smallest available workflow that matches the user's operation and
the code's actual technology boundary. Use one primary skill for an atomic
request and an ordered sequence for a composite request whose stages have
different completion evidence. This skill routes work; it does not duplicate
implementation advice from destination skills.

For every implementation or code review, use pragmatic Clean Code as a
reader-first baseline: domain-revealing names, cohesive responsibilities,
straightforward control flow, and visible contracts, state changes, side
effects, and failures. This baseline does not override a specialist's
correctness constraints or justify unrelated cleanup, mechanical extraction,
or additional abstractions.

## Route in this order

1. Inspect the request, repository instructions, build files, relevant code,
   and tests before selecting a route.
2. Identify the operation: clarify, analyze behavior, diagnose, design or review
   architecture, implement, refactor, test, document, verify, or draft a commit
   message.
3. Identify the boundary: ordinary Java, Spring MVC/blocking, WebFlux/reactive,
   persistence, messaging, security, concurrency, performance, or build system.
4. Decide whether the request is atomic or composite. A request is composite
   only when it explicitly spans distinct operations such as diagnosis, test
   creation, implementation, review, or verification.
5. For an atomic request, choose one primary skill and add one companion only
   when it owns a distinct concern required by the same operation.
6. For a composite request, define the smallest ordered sequence and load only
   the skill for the current stage. Finish or explicitly block that stage
   before loading the next one.
7. Briefly announce `Primary` and optional `Companion` for an atomic request,
   or `Sequence` and the current stage for a composite request, then read and
   follow the selected skill.

Use an explicitly named specialist directly. Do not add this navigator as a
second layer when the route is already unambiguous. Never route to a skill or
connector that is not available in the current environment.

## Sequential workflows

Use a sequence only when the user requested the whole outcome and every stage
remains within that authorization. Do not turn a diagnosis-only request into a
code change, or a review-only request into implementation.

| Composite outcome | Ordered stages |
|---|---|
| Diagnose and fix a concrete failure | `$java-debugging` → `$java-junit` or `$springboot-testing` for a failing regression test when practical → the owning implementation skill → `$java-verification` |
| Implement a clarified ordinary Java behavior with tests | `$behavior-outcome-analysis` only when outcomes remain uncertain → `$maintainable-java-code` or the owning domain skill → `$java-junit` → `$java-verification` |
| Implement a clarified Spring behavior with framework tests | the owning Spring implementation skill → `$springboot-testing` → `$java-verification` |
| Implement an explicitly requested Spring TDD change | `$springboot-tdd` with the owning domain skill as needed → `$java-verification` |
| Review and fix a Java/Spring change set | `$java-code-review` → the owning implementation skill for accepted findings → `$java-verification` |
| Assess, design, and plan service observability | `$observability-workflow`, which owns its internal staged handoffs |

Skip a stage when its result is already established by repository evidence or
the user's approved artifact. Do not rerun a requirements interview merely
because a written requirement is brief. Verification is a terminal evidence
stage, not a permanent companion loaded throughout implementation.

## Primary routes

| Request or evidence | Primary | Optional companion |
|---|---|---|
| Reproduce a concrete failure and identify its root cause | `$java-debugging` | Domain skill only when interpreting or implementing the remedy |
| Module, package, service, dependency, ownership, or deployment boundaries | `$java-architecture-review` | Specialist that owns a material correctness boundary |
| Ordered file-level implementation plan for a clear Java/Spring change | `$java-implementation-planning` | Domain skill only when it must interpret a material specialist contract |
| Diff, pull request, staged change, or pre-merge review across correctness, regression, tests, and maintainability | `$java-code-review` | One domain specialist when a material boundary needs interpretation |
| Ordinary Java implementation or review where clarity and simple design matter | `$maintainable-java-code` | `$effective-java-core` for Java-specific contracts |
| Semantic refactor changing method name, type, validation, sequencing, or exceptions | `$contract-first-refactoring` | `$maintainable-java-code` |
| Java API design, equality, hashing, generics, exceptions, serialization | `$effective-java-core` | `$maintainable-java-code` |
| Shared state, executors, futures, scheduling, cancellation, virtual threads | `$effective-java-concurrency` | `$java-junit` when tests are requested |
| Spring MVC or intentionally blocking Spring service | `$springboot-patterns` | `$springboot-security`, `$jpa-patterns`, or `$maintainable-java-code` |
| WebFlux, Reactor, `Mono`, `Flux`, WebClient, R2DBC, reactive MongoDB, SSE | `$springboot-reactive-patterns` | `$springboot-security` or `$effective-java-concurrency` |
| JPA/Hibernate mappings, transactions, queries, indexing, pagination, pooling | `$jpa-patterns` | `$springboot-patterns` |
| Kafka, RabbitMQ, JMS, SQS, Spring events, outbox, retries, dead letters, message ordering | `$spring-messaging-patterns` | `$jpa-patterns`, `$effective-java-concurrency`, or reactive skill when material |
| Authentication, authorization, CSRF, CORS, secrets, rate limiting, security review | `$springboot-security` | Stack-specific Spring skill |
| Measured latency, throughput, allocation, GC, memory, CPU, contention, or capacity | `$java-performance-engineering` | Specialist that owns the measured bottleneck |
| End-to-end monitoring, SLO, dashboard, alert, logging, tracing, or OpenTelemetry gap assessment and planning | `$observability-workflow` | None; it routes its own focused stages |
| Maven/Gradle, dependencies, BOMs, plugins, toolchains, modules, generated sources | `$java-build-dependency-management` | Domain skill for compatibility interpretation |
| Plain JUnit tests, fixtures, parameterized tests, and test doubles without material Spring semantics | `$java-junit` | Domain skill that defines the behavior |
| Spring MVC/WebFlux, client, serialization, security, persistence, messaging, configuration, or wiring tests | `$springboot-testing` | Domain skill that defines the framework behavior |
| Explicitly requested test-first Spring implementation | `$springboot-tdd` | Domain skill for the changed boundary |
| Build, formatter, static analysis, tests, coverage, security checks, PR/release evidence | `$java-verification` | Domain skill only when results need interpretation |
| Enumerate all observable outcomes from requirements, code, data, and configuration | `$behavior-outcome-analysis` | None unless a separate requirements decision is needed |
| User explicitly wants a probing interview and an approved specification | `$requirements-interview` | None during the interview |
| Source-to-Markdown documentation | `$markdown-docs` | Domain skill only for technical accuracy |
| Staged-diff commit message | `$commit-msg` | None |

For GitHub, issue, pull-request, or CI operations, use an available GitHub tool
or skill only when one is actually present. Otherwise state the capability gap
instead of inventing a route.

## Routing guardrails

- Do not start `$requirements-interview` merely because a feature request is
  brief. Use it when the user wants an interview/specification or a missing
  high-risk decision genuinely prevents safe implementation.
- Do not use `$java-implementation-planning` to hide unresolved product or
  architecture decisions, or when the user asked to implement a plan that is
  already sufficient. Plan only when a planning artifact is the requested
  deliverable or a non-trivial approved change needs decomposition.
- Do not use `$java-junit` to decide what the system can do; derive outcomes
  through `$behavior-outcome-analysis` or the relevant domain contract first.
- Do not use `$java-junit` as the primary route when the claim depends on
  Spring binding, codecs, filters, security, transactions, repositories,
  clients, messaging, configuration, or application wiring. Use
  `$springboot-testing`; reserve `$springboot-tdd` for an explicitly test-first
  production change.
- Do not use `$behavior-outcome-analysis` as a root-cause workflow. Use
  `$java-debugging` when the question is why an observed failure occurs.
- Do not turn a local cleanup into an architecture exercise. Use
  `$java-architecture-review` only when boundaries, dependency direction,
  ownership, deployment, or cross-cutting changeability are material.
- Do not replace `$java-code-review` with `$maintainable-java-code` when the
  request is a general change-set review. The maintainability skill owns
  readability and decomposition, while code review also checks requirements,
  behavior, compatibility, failure paths, tests, and regression risk.
- Do not use blocking Spring/JPA guidance for WebFlux, Reactor, R2DBC, or
  reactive MongoDB.
- Do not add security, persistence, concurrency, or verification companions
  just because the dependency exists. The concern must materially affect the
  requested change.
- Do not activate observability merely because a service has logs or Micrometer
  dependencies. Use it when detection, diagnosis, SLOs, telemetry, dashboards,
  alerts, or instrumentation are part of the requested outcome.
- Follow the project's assertion and test conventions. Prefer AssertJ when it
  is already established, but do not rewrite unrelated tests to enforce a
  global assertion-library preference.
- Check existing project utilities, JDK APIs, framework extension points, and
  installed dependencies before proposing a custom abstraction.
- Use `$maintainable-java-code` as the primary route for ordinary Java. Add it
  to a specialist route only when readability or decomposition is a distinct
  part of the work; do not add it merely to repeat the shared baseline above.

## Stack detection

Use build and source evidence rather than names alone:

- `spring-boot-starter-web` plus servlet types normally indicates Spring MVC.
- Reactor types, WebFlux configuration, or reactive repositories indicate the
  reactive route.
- JPA/JDBC is blocking persistence; R2DBC and reactive MongoDB are reactive.
- Broker clients, listener containers, message annotations, topic/queue
  configuration, or outbox tables indicate the messaging route.
- Security dependencies justify the security route only when authentication,
  authorization, sensitive data, or another security boundary is in scope.
- Maven/Gradle files identify the build system, but route to build management
  only when changing or diagnosing build/dependency behavior. Use verification
  when merely running the existing gate.
- A performance request needs a measurable workload and metric. Route to the
  specialist that owns a confirmed bottleneck only after evidence identifies it.
- Test libraries identify available tools, not the correct test boundary.

## Completion check

- The primary route matches both the requested operation and actual stack.
- An atomic route has at most one companion with a distinct responsibility.
- A composite route loads one stage at a time and gives each stage a completion
  or blocking condition.
- No unavailable skill was selected.
- Routing ends with the next concrete action rather than becoming a separate
  deliverable.
