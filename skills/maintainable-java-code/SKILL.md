---
name: maintainable-java-code
description: Implement or review ordinary production Java code for human readability and long-term maintainability. Use for pragmatic Clean Code work involving clear naming, cohesive responsibilities, simple control flow, explicit contracts, or application flows whose states, side effects, and failures must remain understandable. Use java-junit when the primary deliverable is JUnit tests. Use a narrower concurrency, persistence, security, or reactive skill when that concern determines correctness.
---

# Maintainable Java Code

Produce Java code that a maintainer can understand from its names, types,
contracts, and structure without reconstructing hidden assumptions. Treat Clean
Code principles as reader-focused heuristics rather than fixed rules: optimize
for clear intent and safe change, not short methods, more classes, or visible
use of design patterns.

## Establish the local contract

Before changing code, confirm the target JDK and trace the public entry point,
important callers, prerequisites, data shapes, validation and decision order,
outcomes, state changes, side effects, and failure behavior. Preserve them
unless the request changes the contract. State the smallest behavior change and
verification boundary, and keep unrelated cleanup outside the diff.

Project conventions and explicit requirements win over preferences in this
skill. When the existing design is inconsistent, follow the clearest local
contract and explain any compatibility constraint.

## Design for the reader

- Use domain names that reveal purpose. Avoid vague containers such as
  `data`, `info`, `manager`, `helper`, or `util` unless they are genuinely the
  established domain term.
- Keep each class and method cohesive. A unit may coordinate several steps, but
  it should have one describable responsibility and a consistent abstraction
  level.
- Prefer straightforward control flow. Reduce cognitive branching when the
  existing behavior can be expressed with fewer independent decisions: remove
  redundant or unreachable branches and combine conditions only when they have
  the same outcome. Use guard clauses to reduce nesting, but keep related
  decisions together when splitting or flattening them would hide the rule.
- Preserve materially distinct business outcomes, validation and error
  semantics, and side-effect order. Do not hide real decisions in nested
  ternaries, stream pipelines, lookup maps, or polymorphism solely to lower the
  branch count or a complexity metric.
- Represent materially different states explicitly. Do not use a boolean,
  `null`, or an empty value when callers must distinguish more than two
  outcomes.
- Make side effects, ownership, transaction or lifecycle boundaries, and
  failure behavior visible at the responsible layer.
- Prefer immutable values and narrow visibility when they simplify reasoning.
  Do not add copying, builders, interfaces, or wrappers mechanically.
- Reuse an existing local abstraction only when it already expresses the
  concept clearly. Otherwise prefer suitable JDK or framework facilities before
  adding a custom abstraction for a demonstrated concept or repeated variation.
- Avoid speculative extension points, one-use factories, pass-through layers,
  and generic helpers that erase domain meaning.

Do not apply arbitrary limits for method length, parameter count, or number of
classes. Use cohesion, naming, coupling, and change reasons as the evidence for
refactoring.

## Make application flows readable

When code coordinates meaningful business decisions or effects, read
[references/application-flows.md](references/application-flows.md). Do not load
it for a local calculation or mechanical edit.

## APIs and errors

- Do not expand a public surface without a demonstrated need, and do not shrink
  an existing public contract without an explicitly authorized contract change.
- Use parameter and return types that express the caller's obligations. Validate
  at the boundary that owns the rule and fail before irreversible side effects.
- Preserve useful causes when translating exceptions. Use exceptions for
  exceptional failure, not ordinary branching, and do not collapse distinct
  failures into a generic result for signature convenience.
- Treat equality, hashing, ordering, serialization, and persistence shape as
  contracts when the type participates in them.
- Document externally visible behavior, invariants, units, nullability,
  thread-safety, compatibility, and non-obvious failure semantics. Do not add
  comments that merely repeat the code.

Use `$contract-first-refactoring` when a refactor changes a method name, return
type, validation, sequencing, or exception semantics. Use
`$effective-java-core` for Java-specific API, generics, equality, or exception
details, and `$effective-java-concurrency` when shared state or task lifecycle
determines correctness.

## Verification and self-review

When tests support a production-code change, verify observable behavior and the
failure paths that distinguish its contract. Use `$java-junit` when the primary
deliverable is JUnit tests or when test boundaries, fixtures, parameterization,
assertions, or test doubles require substantial design.

After implementation, read the changed code as a maintainer:

- Can each important name be understood without jumping elsewhere?
- Are invariants and state transitions explicit?
- Can each materially different outcome be mapped to its state changes,
  external effects, and failure behavior?
- Does each abstraction remove more complexity than it introduces?
- Are error and side-effect boundaries visible?
- Is any branch, comment, compatibility shim, or helper now dead or misleading?

After running the repository's required verification, inspect the final diff
for accidental complexity and unrelated changes.

## Deliver the result

For an implementation, summarize the behavior and responsibility changes, the
contracts deliberately preserved, and the verification evidence.

For a review, report concrete maintainability problems in impact order. Include
the location, why a future maintainer is likely to misunderstand or break the
code, and the smallest remedy. Do not manufacture style findings when the code
is already clear.
