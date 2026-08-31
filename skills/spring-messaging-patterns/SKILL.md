---
name: spring-messaging-patterns
description: Design, implement, or review Spring messaging with Kafka, RabbitMQ, JMS, SQS, or Spring application events. Use when message contracts, delivery semantics, ordering, acknowledgements, retries, dead-letter handling, idempotency, outbox publication, schema evolution, or consumer capacity determine correctness; do not use for ordinary synchronous REST calls.
---

# Spring Messaging Patterns

Make asynchronous message behavior explicit from producer state change through
consumer outcome. Inspect the configured Spring, client, broker, and serializer
versions before choosing annotations, container settings, or broker features.

## Establish the message contract

Identify:

- producer, consumer, topic/queue/exchange, key or partition, and payload schema;
- the business event or command meaning and source of truth;
- delivery guarantee actually provided by the broker and client configuration;
- ordering scope, duplicate behavior, acknowledgement or commit boundary;
- retry, timeout, poison-message, dead-letter, replay, and retention behavior;
- transaction, outbox, cache, and external side-effect ordering; and
- throughput, concurrency, capacity, shutdown, and observability owners.

Do not describe a path as exactly-once merely because a broker feature uses
that label. Trace application state and external side effects end to end.

## Choose the boundary deliberately

- Use Spring application events for in-process decoupling only after defining
  whether listeners run synchronously, asynchronously, or after transaction
  commit. They are not a durable broker.
- Use a broker when durability, independent scaling, replay, cross-process
  delivery, or operational isolation is part of the contract.
- Prefer the project's existing Spring abstraction and broker client. Do not
  add a generic messaging wrapper that erases keys, headers, acknowledgements,
  or failure semantics.

## Producer correctness

- Define when publication becomes eligible relative to database commit.
- Avoid an unprotected dual write to the database and broker. Use a transactional
  outbox, broker transaction, change-data capture, or another explicit recovery
  contract when both effects must remain consistent.
- Choose stable event identity, key, timestamp, and schema ownership. Do not
  publish mutable persistence entities as wire contracts.
- Make send failure and confirmation observable. A successful method return is
  not proof of durable broker acceptance unless the client contract says so.

## Consumer correctness

- Make handlers idempotent or define a deduplication owner when redelivery is
  possible. Include the atomicity relationship between deduplication and the
  business write.
- Commit or acknowledge only at the boundary that matches the desired recovery
  behavior. Trace partial side effects before enabling retries.
- Bound concurrency and prefetch against downstream database, HTTP, memory, and
  thread capacity. Preserve per-key ordering when the business contract needs it.
- Classify retryable and terminal failures. Bound attempts and total time, add
  backoff and jitter where appropriate, and define dead-letter ownership,
  alerting, inspection, redrive, and poison-message handling.
- Preserve cancellation, interruption, and graceful shutdown so in-flight work
  is not silently lost or acknowledged early.

Use `$effective-java-concurrency` when executor or shared-state lifecycle is
material, `$jpa-patterns` for transaction and persistence details, and
`$springboot-reactive-patterns` for reactive broker clients and backpressure.

## Schema evolution and security

- Treat event names, payload fields, headers, keys, and serialization as
  compatibility surfaces. Define backward/forward compatibility, unknown
  fields, defaults, producer/consumer rollout order, and removal timing.
- Validate untrusted payload size and shape. Authenticate and authorize broker
  clients with least privilege, protect sensitive fields, and avoid logging full
  messages by default.
- Define retention and deletion requirements for personal or regulated data.

## Testing and verification

Use the smallest test that proves the claim:

- unit tests for pure mapping and idempotency decisions;
- focused listener/container tests for acknowledgement and error mapping;
- broker integration tests for partitioning, serialization, retries, dead
  letters, transactions, or provider-specific behavior; and
- end-to-end tests for database/outbox/publication/consumption consistency.

Test duplicate delivery, out-of-order messages, retry exhaustion, poison data,
consumer restart, partial failure, and shutdown when relevant. Verify metrics
for lag, throughput, retries, dead letters, handler latency, and saturation.

## Deliver the result

State the message contract, consistency and delivery model, ownership of every
retry and terminal path, schema compatibility, capacity assumptions, and the
verification evidence. For a review, report concrete failure scenarios and the
narrowest remedy rather than generic broker best practices.
