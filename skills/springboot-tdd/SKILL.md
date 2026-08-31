---
name: springboot-tdd
description: Implement a Spring Boot feature, bug fix, or refactor test-first when the user requests TDD or the repository explicitly follows a test-first workflow. Select the smallest Spring test boundary that proves the behavior; do not use for verification-only requests.
metadata:
  origin: ECC
---

# Spring Boot TDD

Work in small behavior slices and keep the test boundary aligned with the claim.
Inspect the Spring Boot version, stack, repository test conventions, and
existing fixtures before selecting annotations or utilities; testing APIs and
replacement annotations vary by version.

## Red, green, refactor

1. Describe one externally meaningful behavior, including its important
   failure or empty-state semantics.
2. Add the smallest test that can prove it and run it to confirm it fails for
   the intended reason. A compile error from unfinished scaffolding is not
   sufficient evidence of a behavioral red state.
3. Implement the smallest coherent production change that makes the behavior
   pass without hard-coding the test.
4. Refactor names, responsibilities, duplication, and test setup while keeping
   the focused test green.
5. Repeat for the next materially different outcome, then run the relevant
   module checks.

Do not force a test-first sequence around generated code, mechanical formatting,
or an environment failure that cannot demonstrate the requested behavior.

## Select the boundary

- Plain JUnit: domain decisions and service logic without Spring semantics.
- MVC/WebFlux slice: routing, binding, validation, serialization, status,
  headers, and controller advice. Use the mock-bean facility supported by the
  project's Spring version rather than copying a version-specific annotation.
- Persistence slice or focused integration: mappings, queries, constraints,
  transaction behavior, and database-specific semantics.
- Full application integration: wiring or behavior that genuinely crosses
  several Spring boundaries. Do not use `@SpringBootTest` by default.
- Testcontainers: when the production database, broker, or cache semantics are
  part of the claim. Keep state isolated and lifecycle deterministic; local
  container reuse is an opt-in developer optimization, not a test requirement.

Use `$springboot-reactive-patterns` for publisher, cancellation, timeout, and
backpressure tests, and `$springboot-security` for authentication and
authorization test cases.

## Test design

- Assert observable output, state, transaction result, and required side
  effects. Avoid verifying every internal call.
- Prefer real values and deterministic collaborators. Mock remote or expensive
  boundaries only when isolation is useful; do not mock away serialization,
  persistence, security, or transaction behavior being claimed.
- Use controlled clocks, IDs, schedulers, and containers. Do not use sleeps or
  test-order dependencies.
- Add a fixture builder only when it makes relevant differences easier to see.
  Keep defaults valid and obvious.
- Follow the project's assertion style. Prefer expressive failure messages over
  enforcing a library globally.

Coverage is a diagnostic and a repository-owned gate. Do not introduce or
enforce a universal percentage. Prefer a small set of tests that distinguish
meaningful outcomes over many tests that execute lines without proving behavior.

## Completion

Run the focused test after each slice, then the relevant module suite, formatter,
static checks, and build through the project's existing wrapper. Report the red
evidence, final passing commands, and any integration behavior that remains
unverified.
