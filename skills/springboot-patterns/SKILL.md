---
name: springboot-patterns
description: 'Design, implement, or review Java Spring MVC and intentionally blocking Spring Boot services, including REST boundaries, application layering, validation, caching, blocking clients, and local async work. Do not use for WebFlux/reactive paths or broker/message delivery semantics.'
metadata:
  origin: ECC
---

# Spring Boot MVC and Blocking Services

Design Spring MVC and intentionally blocking services around explicit contracts,
clear ownership, and the project's existing Spring Boot version. Use
`$maintainable-java-code` when ordinary Java readability is the primary concern.

## Scope boundary

This skill is for Spring MVC/servlet-stack or intentionally blocking paths. For WebFlux, Reactor, `Mono`, `Flux`, `WebClient`, R2DBC, or reactive MongoDB, use `$springboot-reactive-patterns`; do not apply blocking examples from this skill to a reactive pipeline. For Kafka, RabbitMQ, JMS, SQS, Spring application events, outbox publication, or message delivery semantics, use `$spring-messaging-patterns`.

## Framework-first implementation

Before creating a helper, wrapper, factory, or custom abstraction, inspect the existing project and the active Spring/JDK APIs. Prefer Spring MVC, Spring Boot, Spring Data, Bean Validation, Spring's transaction and scheduling facilities, and existing project utilities when they match the required behavior. Use JDK APIs when they are clearer for generic logic. Do not add a Spring utility solely for style, and do not build a custom framework around a feature Spring already owns. Check the project's actual dependency version and extension point before coding.

For tests, use the project's Spring test support and established assertion
style. Do not rewrite unrelated tests merely to standardize an assertion
library.

## Responsibility boundaries

- Controllers own HTTP binding, validation activation, status/headers, and
  translation to application inputs and outputs. They should not own business
  decisions or persistence orchestration.
- Application services own use-case sequencing, transaction boundaries, and
  coordination of domain behavior and external ports.
- Domain code owns business invariants that remain meaningful without Spring.
- Repositories and clients own persistence or remote protocol details; do not
  leak their representations and exceptions through every layer.

Use the smallest number of layers that keeps these responsibilities clear. A
pass-through service or mapper with no contract is not automatically useful.

## When to Activate

- Building REST APIs with Spring MVC or servlet-stack Spring Boot
- Structuring controller → service → repository layers
- Configuring Spring Data JPA, caching, or async processing
- Adding validation, exception handling, or pagination
- Setting up profiles for dev/staging/production environments
- Coordinating blocking clients, local async work, or time-triggered jobs

## HTTP, service, and data boundaries

- Define request and response types from the public API contract. Do not expose
  entities or accept persistence models as request bodies.
- Apply Bean Validation to syntactic and boundary constraints. Keep business
  invariants in the domain/application layer and return stable field/error
  structures rather than concatenated framework messages when clients depend on
  them.
- Use constructor injection and require collaborators that are part of the
  component's valid state.
- Put transactions around a coherent use case. Do not rely on controller
  lifetime, Open Session in View, or incidental lazy loading to complete the
  response.
- Use Spring Data derived queries, explicit JPQL, specifications, projections,
  and pageable types only when they express the actual query contract. Route
  persistence-specific decisions to `$jpa-patterns`.

## Exception mapping

Centralize HTTP exception translation when several endpoints share the same
contract. Distinguish validation, missing resources, conflicts, authorization,
dependency failure, and unexpected defects. Preserve safe diagnostic context
and the original cause internally; never send raw exception messages or stack
traces to clients. Prefer RFC 9457 problem details when the configured Spring
version and existing API contract use them.

## Caching

Add caching only after defining key identity, value ownership, staleness,
eviction on every write path, null/absence behavior, transaction timing, and
multi-instance consistency. Use the project's existing cache manager and
serialization. Do not create an empty cache-eviction service or add annotations
without tracing invalidation and failure behavior.

## Async processing

Use `@Async` only when asynchronous completion is part of the contract. Define
the executor owner, capacity, rejection behavior, exception observation,
context propagation, transaction/event timing, cancellation, and shutdown.
Avoid self-invocation assumptions and fire-and-forget work whose failure is
invisible. Use `$effective-java-concurrency` when those decisions are material.

## Logging, filters, and pagination

- Use the project's structured logging and observability conventions. Add
  operation-specific context once, without secrets or personal data. Avoid
  catching a broad exception only to log and rethrow when a central boundary
  already records the same failure.
- Add servlet filters only for truly cross-cutting HTTP behavior and define
  ordering, async/error dispatch handling, request-body implications, and
  security-filter interaction.
- Validate page size and allowed sort fields. Use deterministic ordering with a
  stable tie-breaker. Do not expose arbitrary entity property names as a public
  sorting API.

## External calls and resilience

Set connect, response, and overall deadlines at the owning client boundary.
Use the project's configured resilience library or Spring facility rather than
a generic `Thread.sleep` retry helper. Retry only classified transient failures
and operations that are idempotent or protected by an idempotency contract.
Bound attempts and total time, add jitter when shared dependencies are involved,
preserve interruption, and make exhaustion observable.

## Rate limiting

Do not copy an unbounded per-IP `ConcurrentHashMap` limiter into production. It
leaks cardinality, is inconsistent across instances, and often identifies a
proxy rather than the caller. Prefer a gateway or shared bounded limiter. If an
in-process limiter is deliberately sufficient, define bounded eviction,
trusted-proxy handling, stable identity, distributed limitations, retry hints,
metrics, and tests. Use `$springboot-security` for the threat model.

## Background Jobs

Use Spring's `@Scheduled` for time-triggered work only after defining overlap,
cluster ownership, misfire/catch-up behavior, idempotency, failure observation,
and shutdown. Use `$spring-messaging-patterns` for broker-backed queues and
message delivery.

## Observability

Use the repository's established logging, metrics, and tracing stack. Add a
signal only when it helps detect, localize, or explain a named failure mode;
keep dimensions bounded and sensitive data out. Use `$observability-workflow`
for an end-to-end gap assessment, SLO/dashboard/alert design, or OpenTelemetry
implementation plan rather than introducing a backend or logging format here.

## Production Defaults

- Prefer constructor injection, avoid field injection
- Prefer Spring `ProblemDetail` when the configured version and existing API
  contract use RFC 9457 problem details
- Configure HikariCP pool sizes for workload, set timeouts
- Put transactions around use cases that require atomicity; use read-only hints
  only when their semantics and provider behavior are understood
- Express nullability through the project's established annotations and API
  contracts rather than adding `Optional` mechanically

Before finishing, verify validation and exception mapping, transaction and side-
effect ordering, timeout/retry behavior, sensitive logging, and the relevant
formatter, build, and tests. Prefer clear responsibilities over a blanket rule
that every controller must be thin or every repository must be simple.
