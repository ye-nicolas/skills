---
name: jpa-patterns
description: Design or review JPA/Hibernate entities, relationships, fetch plans, transactions, queries, pagination, migrations, and connection capacity in Spring Boot. Use when persistence semantics materially affect the change; do not use for R2DBC or reactive persistence.
metadata:
  origin: ECC
---

# JPA/Hibernate Persistence

Start from the database contract, production database, configured Hibernate and
Spring Data versions, transaction boundaries, and actual query paths. Do not
copy mapping, pool, or batching values without evidence from the target system.

## Framework-first persistence

Before creating a repository helper, query abstraction, transaction wrapper, audit mechanism, pagination type, or pool manager, inspect the existing project and the Spring Data/JPA/Hibernate APIs for the configured versions. Prefer `JpaRepository`, derived queries, `Specification`, projections, `Pageable`, auditing, `@Transactional`, entity callbacks, database constraints, and provider-supported features when they match the requirement. Do not add a custom abstraction for one repository or one query without a demonstrated need. Use native SQL only when the ORM/provider cannot express the required query and document the trade-off.

For persistence tests, use the project's Spring test slices and integration
support. Follow its assertion conventions and use the production database type
when provider-specific behavior is part of the claim.

## Entity boundaries

- Keep persistence concerns visible, but do not let entities expose mutable
  collections or unrestricted setters that bypass domain invariants.
- Define constructors/factories and relationship helper methods that keep both
  sides consistent when the object model is bidirectional.
- Base equality on a stable identity/value contract. Do not include lazy
  collections or mutable associations, and account for generated identifier and
  proxy lifecycle before overriding `equals`/`hashCode`.
- Use `EnumType.STRING` only with a compatibility plan for renames and unknown
  values. Treat column names, lengths, precision, nullability, and constraints
  as schema contracts, not documentation.

## When to Activate

- Designing JPA entities and table mappings
- Defining relationships (@OneToMany, @ManyToOne, @ManyToMany)
- Optimizing queries (N+1 prevention, fetch strategies, projections)
- Configuring transactions, auditing, or soft deletes
- Setting up pagination, sorting, or custom repository methods
- Tuning connection pooling (HikariCP) or second-level caching

## Relationships and fetch plans

- Make associations lazy unless a proven invariant requires otherwise, then
  choose an explicit fetch plan per use case.
- Avoid `EAGER` collections. Use entity graphs, fetch joins, batch fetching, or
  projections according to cardinality and update/read needs.
- Use cascade and orphan removal only for entities with the same lifecycle
  owner. Keep bidirectional associations consistent through methods on the
  owning aggregate.
- Diagnose N+1 from the actual access path and generated SQL. Avoid solving it
  with global eager loading or one fetch plan reused by every endpoint.
- Do not combine collection fetch joins with pageable queries unless duplicate
  rows, limits, and count-query behavior are explicitly handled.

## Repository queries

Use the least complex Spring Data mechanism that keeps the query readable:
derived methods for short stable predicates, explicit JPQL/entity graphs for
controlled fetch behavior, specifications for genuine composable criteria, and
native SQL only for database features the ORM cannot express. Use projections
when a read contract needs a stable subset or aggregation; do not create one for
every query.

## Transactions

- Put `@Transactional` around application use cases that require atomicity,
  not every service method mechanically.
- Keep remote calls, unbounded work, and user interaction outside database
  transactions unless the consistency contract explicitly requires them.
- Use `readOnly = true` as an intentional semantic/provider hint after checking
  actual behavior; do not assume it is a universal performance optimization or
  enforcement mechanism.
- Define rollback, isolation, propagation, optimistic/pessimistic locking, and
  event publication from the concurrency and failure contract.

## Pagination

For keyset pagination, use a deterministic sort and carry the complete last-seen
sort tuple, including a unique tie-breaker. A lone `id > :lastId` is correct only
when ascending ID is the actual ordering contract. Validate public page sizes
and sort fields. Use offset pagination when its navigation and scale trade-offs
fit; do not implement keyset pagination without a stable continuation contract.

## Indexing and Performance

- Add indexes from observed query predicates, join/order patterns, selectivity,
  write cost, and an actual execution plan.
- Use projections when they make ownership and data shape clearer; do not add
  one for every query or assume ORM entity loading always emits `select *` in a
  harmful way.
- Treat `saveAll` as an API convenience, not proof of JDBC batching. Verify ID
  generation strategy, configured batch size/order, flush/clear behavior,
  transaction size, and generated SQL under representative load.

## Connection pooling

Do not prescribe universal HikariCP numbers. Size the pool from database
capacity shared across application instances, measured concurrent demand,
transaction duration, acquisition timeout, and overload behavior. Monitor
active/idle connections, wait time, timeouts, database saturation, and leak
signals. Add vendor-specific Hibernate properties only for a demonstrated
driver/provider requirement.

## Caching

- 1st-level cache is per EntityManager; avoid keeping entities across transactions
- For read-heavy entities, consider second-level cache cautiously; validate eviction strategy

## Migrations

- Use the repository's established migration mechanism. If production schema
  evolution is required and none exists, recommend a reviewed migration tool
  and rollout workflow rather than adding Flyway or Liquibase implicitly. Do
  not rely on Hibernate auto DDL to manage production schema changes.
- Make migrations ordered, reviewable, and compatible with the deployment
  strategy. Prefer expand/migrate/contract for rolling changes. Define rollback
  or forward-fix behavior, data backfill observability, and a removal plan for
  destructive schema changes; do not assume every migration can be idempotent.

## Testing Data Access

- Use `@DataJpaTest` or the project's focused persistence-test support. Use a
  container or managed test database when production database semantics are
  part of the claim; do not require it for a pure repository contract that the
  existing test environment already proves.
- Inspect generated SQL, query counts, and plans through test tooling or
  temporary controlled diagnostics. Do not enable bind-value TRACE globally;
  parameters may contain credentials or personal data.

Before finishing, verify mappings and constraints against the production
database type, transaction rollback and concurrency behavior, query count and
pagination semantics, migration compatibility, and the relevant project tests.
