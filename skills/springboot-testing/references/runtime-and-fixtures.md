# Spring Test Runtime and Fixtures

Read this reference when context lifecycle, infrastructure, time, concurrency,
or shared fixtures materially affect the test.

## Context reuse

Spring caches application contexts by their effective configuration. Reuse the
same slice annotations, properties, profiles, imports, and mock definitions for
tests with the same boundary. Create a new context only when the changed
configuration is part of the claim. Avoid broad dirty-context markers; identify
and reset the actual mutable state when practical.

## Infrastructure

- Reuse the repository's container lifecycle and production-compatible image
  policy. Do not add Testcontainers solely because it is familiar.
- Isolate database schemas, topics, queues, cache keys, ports, and test data so
  parallel runs cannot interfere.
- Wait for observable readiness rather than sleeping. Bound startup and request
  timeouts and preserve diagnostic output on failure.
- Close only resources owned by the test. Confirm application-managed pools,
  clients, executors, and containers reach their expected lifecycle state.

## Deterministic fixtures

- Keep fixture defaults valid and explicit. Builders should highlight values
  that change the scenario rather than hide required state.
- Use controlled `Clock`, IDs, schedulers, and executors. Use Reactor virtual
  time or framework scheduling controls for time-based behavior.
- Prefer real request, response, entity, event, and value types. Use a fake or
  stub when it communicates state more clearly than interaction-heavy mocks.
- Make cleanup resilient to a failed assertion without deleting shared or
  developer-owned data.

## Failure diagnosis

When a test fails, distinguish assertion failure from context startup,
dependency resolution, container readiness, port collision, leaked thread,
transaction cleanup, or environment restriction. Do not weaken the assertion
or production contract to hide an infrastructure failure.
