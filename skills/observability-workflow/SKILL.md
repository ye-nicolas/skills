---
name: observability-workflow
description: "Coordinate an evidence-first observability workflow for an existing service: assess gaps, design SLOs/dashboards/alerts, and map approved improvements to OpenTelemetry instrumentation. Use for end-to-end observability reviews, especially Java/Spring systems; use the focused skills directly for a single instrumentation or dashboard task."
---

# Observability Workflow

Coordinate the installed observability skills as one workflow. The objective is
to answer three different questions in order:

1. **What is missing or unreliable?** — use `observability`.
2. **What should the target operating model look like?** — use
   `observability-designer`.
3. **How should the application emit the required telemetry?** — use
   `otel-instrumentation`.

Do not collapse these questions into a generic list of best practices. Carry
evidence and decisions from one stage to the next.

## Routing

Choose the smallest workflow that satisfies the request:

- **Assessment only** (`盤點`, `缺什麼`, `review`, `audit`) — run Stage 1 and
  stop after the findings and limitations.
- **Assessment and design** (`規劃`, `設計`, `SLO`, `dashboard`, `alert`) —
  run Stages 1–2 for the highest-priority findings.
- **Implementation planning** (`如何落地`, `加 instrumentation`, `加 OTel`) —
  run Stages 1–3 and produce a file-level implementation plan.
- **Complete workflow** (`完整盤點與方案`, `從頭規劃`) — run all three stages.

Use a focused skill directly when the user asks only for one narrow task, such
as fixing a broken span, writing one dashboard, or designing one SLO. This
workflow is for connecting assessment, design, and instrumentation.

## Stage 0 — Establish scope

Before delegating work:

- Identify the repository, revision, deployment environment, and observability
  backend/configuration that are in scope.
- Determine whether the request is static repository review, live telemetry
  review, or both. Never claim live evidence when only files are available.
- Identify critical user journeys or, if none are named, infer candidates from
  externally visible entry points and clearly label the inference.
- For Java/Spring repositories, keep the Java/Spring review lens active through
  all stages. The `observability` skill contains the stack-specific reference.

Ask only the minimum questions whose answers would materially change the
assessment. If the user says to proceed, state assumptions instead.

## Stage 1 — Discover gaps with `observability`

Explicitly load and follow the installed `observability` skill first.

It must:

- inspect the service paths and existing monitoring, logging, tracing,
  dashboard, alert, SLO, and runbook definitions;
- map each important failure mode to the signal that should detect, localize,
  or explain it;
- distinguish missing coverage, unusable/noisy coverage, and unverified
  coverage;
- produce a scope statement, an evidence-backed findings table, confidence, and
  explicit limitations;
- remain read-only during assessment.

Do not continue to design every possible signal. Carry only the highest-value
findings and their evidence into Stage 2.

## Stage 2 — Turn selected gaps into a target design

For selected findings, explicitly load and follow `observability-designer`.

Pass it the Stage 1 evidence and preserve existing coverage. Ask it to produce,
as applicable:

- user-impact-oriented SLI/SLO and error-budget definitions;
- symptom-based alerts with severity, routing, threshold rationale, and
  runbook links;
- dashboard views that move from service health to the failing component;
- structured log and trace-correlation requirements;
- sampling, retention, cardinality, and telemetry-cost decisions.

If criticality, audience, or user-facing status is unknown, use explicit
assumptions or ask only the two or three questions that materially change the
design. Do not let the design skill invent facts about the current system.

## Stage 3 — Map the design to instrumentation

Load and follow `otel-instrumentation` only for the signals and services
selected in Stage 2.

For Java/Spring, inspect and map the design to the actual application surface:

- Spring MVC/WebFlux entry points and error handling;
- outbound HTTP clients and service-to-service context propagation;
- JDBC/JPA/Hibernate, HikariCP, Redis, and other data stores;
- Kafka/RabbitMQ/JMS/SQS publishing, consumption, retry, and dead-letter paths;
- `@Async`, schedulers, executors, virtual threads, and batch jobs;
- Actuator, Micrometer, OpenTelemetry agent/SDK, exporters, Collector, and
  deployment configuration;
- JVM, GC, thread-pool, connection-pool, queue-lag, and saturation signals.

Check resource identity, semantic conventions, bounded metric dimensions,
sensitive-data handling, duplicate instrumentation, sampling, export failure,
and post-change validation. Prefer the smallest instrumentation change that
fulfills the approved design.

## Handoff rules

- Stage 1 findings are the evidence source of truth. Do not restate a suspected
  gap as fact after handoff.
- Stage 2 defines the desired operational behavior; it does not silently change
  application architecture or invent a backend.
- Stage 3 maps the design to code and runtime configuration; it does not weaken
  an SLO or remove a signal merely because implementation is inconvenient.
- If a stage cannot verify something, mark it as an assumption or an
  investigation item and state what evidence is needed.

## Default side-effect boundary

The default workflow is advisory and read-only. Do not edit application code,
infrastructure, dashboards, alert rules, collector configuration, or deployment
manifests unless the user explicitly asks for implementation. A planning run may
write only the requested review/plan artifacts and must state their location.
Never reproduce secrets or sensitive telemetry values.

## Final output

For a complete workflow, report in this order:

1. **Scope and assumptions** — repository/revision, environments, tools,
   critical journeys, and what was not examined.
2. **Current-state summary** — existing signals and known operational coverage.
3. **Prioritized findings** — evidence, impact, effort, risk, confidence, and
   the named failure mode each finding addresses.
4. **Target design** — selected SLI/SLO, dashboard, alert, log, trace, sampling,
   retention, and runbook decisions.
5. **Instrumentation mapping** — concrete Java/Spring/OpenTelemetry locations,
   required attributes, propagation boundaries, and data-safety constraints.
6. **Implementation backlog** — ordered changes with validation and rollback
   criteria.
7. **Verification gaps** — live access, backend state, or production evidence
   still required.

For an assessment-only request, stop after item 3 and the verification gaps.
