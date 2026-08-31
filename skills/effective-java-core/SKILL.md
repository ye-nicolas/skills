---
name: effective-java-core
description: Apply current, project-aware Java design practices when writing or reviewing APIs, value types, equality, generics, exceptions, object lifecycle, and serialization. Use for Java-specific correctness and API contracts; use maintainable-java-code for general readability and effective-java-concurrency for concurrent paths.
---

# Effective Java Core

Apply Java-specific design guidance only after checking the repository's target
JDK, compatibility policy, public callers, and established conventions. Do not
introduce a newer language or library feature unless the configured toolchain
supports it.

Use `$maintainable-java-code` for general readability and decomposition. Use
`$effective-java-concurrency` for shared state, executors, futures, scheduling,
or thread lifecycle.

## Review the contract first

1. Identify the externally visible API and all important callers.
2. Map valid inputs, absence/null semantics, return states, exceptions, side
   effects, mutability, lifecycle, and compatibility constraints.
3. Choose the smallest Java type and API shape that expresses those facts.
4. Preserve behavior unless the request explicitly changes it; update callers,
   tests, and documentation together when it does.

## Object and API design

- Keep visibility narrow and expose behavior rather than mutable
  representation.
- Prefer immutable value objects when identity and lifecycle do not require
  mutation. Use defensive copies only at real mutable boundaries.
- Choose constructors, named factories, records, or builders according to the
  actual invariants and call-site readability. Do not add a builder for a small
  stable value or a factory that provides no naming, lifecycle, or subtype
  benefit.
- Favor composition when inheritance would expose implementation details or
  create fragile override contracts. Design inheritance deliberately when it
  is part of the supported API.
- Introduce an interface for a real substitutable role or boundary, not solely
  for mocking or to satisfy a blanket layering rule.
- Use try-with-resources for owned `AutoCloseable` resources. Close only what
  the component owns.

## Values, equality, and ordering

- Define equality from stable logical identity or value semantics. When
  overriding `equals`, implement a consistent `hashCode` and test both.
- Exclude mutable associations, caches, generated identifiers without stable
  lifecycle semantics, and sensitive data from equality or diagnostic output.
- Make ordering consistent with equality when callers rely on sorted sets or
  maps. Use comparator composition rather than arithmetic subtraction.
- Make `toString` useful for diagnostics without leaking secrets or creating an
  undocumented interchange format.

## Types and collections

- Avoid raw types. Keep unchecked casts local, justified, and protected by a
  runtime invariant or focused test.
- Use bounded wildcards when they make an API more usable; do not make a local
  implementation generic without a real second type use case.
- Prefer domain types, enums, and value objects when strings or booleans would
  hide states, units, or validation rules.
- Return empty collections for a successful zero-result query. Use `Optional`
  for a meaningful absent return value when it clarifies the caller contract;
  do not use it mechanically for fields, parameters, or every nullable boundary.
- Avoid exposing mutable collections. Return an immutable value or documented
  snapshot when callers must not modify internal state.

## Methods and failures

- Validate at the boundary that owns the precondition and before irreversible
  side effects. Use messages with safe diagnostic context.
- Keep overloads unambiguous at call sites. Prefer distinct names or parameter
  objects when overload resolution or boolean arguments obscure meaning.
- Choose checked, unchecked, or result-based failure according to the caller's
  recovery obligation and existing project contract; there is no universal
  mapping from "recoverable" to checked exception.
- Translate lower-level failures at an abstraction boundary only when the new
  exception adds domain meaning. Preserve the cause and do not catch broad
  exceptions merely to log and rethrow.
- Leave state valid after failure and make partial side effects explicit when
  atomicity is impossible.

## Serialization and compatibility

Treat Java serialization, JSON shape, database representation, and published
method signatures as compatibility surfaces. Avoid native Java serialization
for new designs unless a concrete integration requires it. When a serialized
form already exists, preserve invariants, versioning, unknown-field behavior,
and security constraints deliberately.

## Verification

Verify the changed contract with focused tests for normal, absent, invalid, and
failure cases. Compile against the configured JDK, run project checks, and
inspect the final diff for unnecessary API growth or version-dependent code.
