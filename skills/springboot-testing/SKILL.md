---
name: springboot-testing
description: Design and implement focused Spring Boot tests when framework behavior is part of the claim, including MVC/WebFlux HTTP contracts, serialization, clients, security, persistence, messaging, configuration, and application wiring. Use for test-focused work that is not an explicitly test-first production change. Use java-junit for plain Java tests and springboot-tdd for an explicitly requested TDD implementation workflow.
---

# Spring Boot Testing

Write tests that prove the Spring behavior callers and operators rely on without
loading more framework or infrastructure than the claim requires. Follow the
repository's Spring Boot, Spring Framework, JUnit, assertion, fixture, and build
conventions rather than assuming the latest test API.

## Establish the framework contract

Inspect the configured Spring Boot and dependency versions, MVC versus WebFlux
stack, test source sets, existing annotations and utilities, production
database or broker, container support, profiles, and repository verification
commands. Trace the public behavior through binding, validation, serialization,
filters, security, transactions, repositories, clients, messages, scheduling,
and exception mapping that actually participate in the claim.

State the observable behavior, important alternate or failure outcomes, and the
framework mechanism that must be real in the test. Do not select
`@SpringBootTest`, a slice, a mock, or a container before that boundary is
clear.

## Select the smallest proving boundary

Read [test boundaries](references/test-boundaries.md) to choose among plain
JUnit, Spring slices, focused integration, and full application tests. Keep the
mechanism being claimed real:

- do not mock MVC/WebFlux binding, codecs, controller advice, filters, or the
  security chain when their behavior is under test;
- do not replace JPA mappings, database constraints, transactions, broker
  acknowledgements, or serialization with mocks when those semantics matter;
- mock or stub remote and expensive boundaries when isolation improves the
  claim and their protocol behavior is not being tested; and
- use a production-like database, broker, cache, or container only when its
  provider-specific behavior affects correctness.

Use `$java-junit` when Spring semantics are not part of the claim. Use
`$springboot-tdd` when the user requests a red-green-refactor production change
or the repository explicitly requires test-first implementation.

## Keep tests deterministic and maintainable

Read [runtime and fixture guidance](references/runtime-and-fixtures.md) when
the test uses application contexts, containers, time, asynchronous work, or
shared fixtures.

- Assert status, headers, body, signals, state, transaction result, and required
  side effects that form the public contract; avoid verifying every internal
  interaction.
- Follow the repository's assertion style. Prefer existing builders and
  fixtures when their defaults remain visible and valid.
- Control clocks, IDs, schedulers, executors, ports, and external responses.
  Do not use sleeps, test-order dependencies, or shared mutable state.
- Keep context customizations stable so equivalent tests can reuse the Spring
  context cache. Do not add a distinct profile or mock set to every class.
- Use the mock-bean replacement and test-client APIs supported by the detected
  Spring version. Do not migrate unrelated tests to a newer annotation or API.
- Treat disabled tests, retries, and broad exception assertions as unresolved
  evidence, not passing coverage.

## Specialist boundaries

Use one companion when it defines the tested contract:

- `$springboot-patterns` for MVC, blocking clients, caching, jobs, and service
  boundaries;
- `$springboot-reactive-patterns` for publisher cardinality, timeout, retry,
  cancellation, backpressure, and virtual time;
- `$jpa-patterns` for mappings, queries, transactions, constraints, locking,
  migrations, and database-specific behavior;
- `$springboot-security` for authentication, authorization, CSRF/CORS, tenant,
  and sensitive-data cases;
- `$spring-messaging-patterns` for serialization, delivery, acknowledgement,
  retry, dead-letter, ordering, and idempotency; and
- `$effective-java-concurrency` for deterministic shared-state or executor
  lifecycle tests.

## Implement and verify

1. Add the smallest test that proves one materially distinct outcome.
2. Run it through the repository's wrapper and confirm any intended regression
   or TDD red state fails for the expected behavioral reason.
3. Make only test or fixture changes when tests are the requested deliverable;
   do not change production behavior merely to make an incorrect expectation
   pass.
4. Run the focused test, then the affected slice, module, or integration suite
   when the changed test boundary or risk warrants it.
5. Inspect logs and reports for context startup, resource, thread, container,
   and cleanup failures that a nominal pass may hide.

Report the behavior proven, selected boundary and why it is sufficient, exact
commands and results, infrastructure used, and any framework or provider
behavior that remains unverified.
