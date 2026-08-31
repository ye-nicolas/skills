---
name: java-junit
description: Design and implement focused JUnit 5 tests for observable plain Java behavior, including parameterized cases, deterministic fixtures, and appropriate test doubles. Follow the project's existing test and assertion conventions. Use springboot-testing when binding, serialization, security, persistence, messaging, configuration, or other Spring framework semantics are part of the claim.
---

# JUnit 5 Test Design

Write tests that explain the behavior a maintainer may safely depend on. Follow
the repository's JUnit version, source layout, naming, fixture, assertion, and
build conventions before applying preferences from this skill.

## Choose the test boundary

1. State the observable behavior, preconditions, and materially different
   outcomes before writing the test.
2. Use a unit test for pure decisions, transformations, and small object
   contracts.
3. Use `$springboot-testing` when the claim depends on Spring binding,
   serialization, filters, security, transactions, repositories, clients,
   messaging, configuration, scheduling, or application wiring. Use the
   relevant domain skill for non-Spring integration, contract, concurrency, or
   system boundaries.
4. Test at the narrowest boundary that can prove the plain Java claim; do not
   mock away the behavior under test.

## Make tests readable

- Give the test a name that states the expected behavior and relevant scenario.
  Follow the project's naming style. Add `@DisplayName` only when it is clearer
  than the Java identifier or the project already uses it.
- Keep setup focused on facts that matter to the behavior. Prefer builders or
  fixture methods only when they remove repetition without hiding important
  values.
- Separate setup, action, and assertions visually when that helps the reader;
  do not force comments or ceremony into a short test.
- Assert the complete meaningful outcome: return value or exception, changed
  state, and required side effects. Avoid broad snapshots or incidental fields
  that make harmless refactors fail.
- Keep tests independent of execution order and shared mutable state. If a flow
  is inherently sequential, test it as one scenario rather than ordering test
  methods.

## Parameterized tests

Use `@ParameterizedTest` when several inputs exercise the same behavior and
produce failures that remain easy to diagnose. Use the smallest source that
keeps cases legible:

- `@ValueSource` or `@EnumSource` for one simple dimension.
- `@CsvSource` for a few scalar values whose quoting remains clear.
- `@MethodSource` for domain objects, nulls, expected exceptions, or cases that
  deserve names.

Split cases into separate tests when they represent different contracts or
need substantially different setup and assertions.

## Assertions and test doubles

- Use the assertion style already established by the project. Prefer AssertJ
  when available and when its domain/collection assertions improve failure
  messages; do not rewrite unrelated tests solely to enforce one library.
- Prefer real values and deterministic collaborators. Use a fake or stub when
  it communicates state more clearly than a mock.
- Mock an external or expensive boundary when isolation is useful. Stub only
  behavior the scenario needs, and verify interactions only when the interaction
  itself is part of the contract.
- Do not create an interface solely for Mockito. Do not use partial mocks to
  reach private implementation details.
- Use controlled clocks, IDs, schedulers, and executors instead of sleeps or
  timing luck.

## Verification

Run the focused test through the repository's wrapper, then the relevant module
suite when risk warrants it. Check that the test fails for the intended reason
before the fix when doing TDD or regression work, and report any unverified
framework or integration behavior explicitly.
