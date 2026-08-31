# Test Doubles

Use this chapter only when you are writing or modifying tests.

Choose the smallest test boundary that proves the behavior without coupling the
test to implementation details.

- Prefer real domain values and deterministic collaborators when they are
  inexpensive and make the test clearer.
- Use a small fake or stub when it expresses state and behavior more clearly
  than interaction-heavy mocking.
- Mock remote clients, clocks, nondeterministic services, expensive resources,
  and other external boundaries when isolation is useful. Mock the contract
  the production code actually depends on; do not introduce an interface only
  to satisfy a mocking framework.
- Use the real database through the project's integration-test support when
  database constraints, mappings, transactions, query behavior, or migrations
  are part of the claim. Testcontainers is one option, not a requirement for
  every integration test.
- Verify outcomes and meaningful side effects. Verify calls only when the
  interaction itself is part of the contract.

For Spring Data JPA projection-shaped test data, prefer a direct anonymous
implementation when it is clearer than a mock, for example
`new SomeProjectionVo() { ... }`. Do not mock projection data, and do not create
a separate record/class solely to implement the projection interface.
