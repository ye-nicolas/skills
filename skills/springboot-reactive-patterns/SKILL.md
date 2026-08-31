---
name: springboot-reactive-patterns
description: Design, implement, and review Java Spring WebFlux and Reactor code using non-blocking composition, WebClient, reactive data access, backpressure, cancellation, context propagation, resilience, and reactive testing. Use for Mono, Flux, Publisher, R2DBC, reactive MongoDB, SSE, and other reactive Spring Boot paths; do not use for Spring MVC or blocking JPA/JDBC code.
---

# Spring Boot Reactive Patterns

Use this skill for Spring WebFlux and Reactor applications where the request path is intended to remain non-blocking. Treat `Mono<T>` as an asynchronous 0-or-1 result and `Flux<T>` as an asynchronous 0-to-many sequence; keep that cardinality visible in APIs and tests.

## Activation and scope

Activate for:

- Spring WebFlux annotated controllers or functional endpoints.
- Reactor operators, `Mono`, `Flux`, `Publisher`, `Scheduler`, or `Context`.
- `WebClient`, reactive HTTP streaming, WebSocket/RSocket, or SSE.
- Reactive Spring Data such as R2DBC or reactive MongoDB.
- Reactive resilience, rate limiting, backpressure, cancellation, or non-blocking tests.

For servlet-stack Spring MVC, synchronous service methods, JPA, JDBC, or blocking libraries, use `$springboot-patterns` and `$jpa-patterns` instead. Use `$effective-java-concurrency` as a companion when the change also involves shared state or executor lifecycle.

## Framework-first implementation

Before creating a custom reactive helper, inspect the project's existing operators and the active Spring/Reactor APIs. Prefer WebFlux controller and codec support, `WebClient` builders and filters, Reactor operators, `Retry`, `Context`, `Scheduler`, reactive transaction operators, and existing project utilities when they express the required behavior. Use a custom abstraction only when the native API cannot express the contract; document the missing capability. Verify the project's Reactor and Spring versions before selecting an operator or extension point.

For reactive tests, use `WebTestClient`, `StepVerifier`, and Reactor test
utilities. Follow the project's assertion conventions for ordinary values;
prefer AssertJ when it is established and improves diagnostics.

## Non-blocking contract

1. Keep blocking calls off event-loop threads. Do not use `Thread.sleep`, `Future.get`, synchronous JDBC/JPA, file I/O, or other blocking APIs inside a reactive operator.
2. Do not call `.block()`, `.blockOptional()`, `.toIterable()`, or `.toStream()` in application request paths. Return or compose the publisher instead.
3. If a blocking dependency cannot be removed, isolate the smallest call with `Mono.fromCallable(...)` and `subscribeOn(Schedulers.boundedElastic())`. Bound the work, set a timeout, document the dependency, and measure the queue and latency impact.
4. Preserve cancellation. Avoid starting side effects with an unmanaged `subscribe()` inside application code; compose the publisher so the framework owns subscription and cancellation.
5. Keep mutable state local to a subscription or protect it explicitly. Do not assume a request stays on one thread.

Example of an explicit blocking boundary:

```java
Mono<Account> account = Mono.fromCallable(() -> legacyAccountClient.load(id))
    .subscribeOn(Schedulers.boundedElastic())
    .timeout(Duration.ofSeconds(2));
```

Prefer a reactive client or repository when one exists. `boundedElastic()` is an escape hatch, not a way to hide unbounded blocking work.

## Composition and operator choice

- Use `map` for a synchronous, non-blocking transformation and `flatMap` when the transformation returns a publisher.
- Use `concatMap` when order matters or downstream capacity is limited. Use `flatMap(fn, concurrency)` when parallelism is intentional and bounded.
- Use `switchIfEmpty(Mono.defer(() -> fallback()))` when the fallback must be created or invoked only after the source is known to be empty.
- Use `timeout` at an externally meaningful boundary and translate the failure into the API's error contract.
- Use `onErrorMap` to add domain meaning, `onErrorResume` for a deliberate fallback, and `doOnError` only for side effects such as metrics or logging.
- Keep a cold publisher cold unless sharing is intentional. For `cache`, `share`, `publish`, or `replay`, define ownership, lifetime, replay behavior, and invalidation.
- Do not use `parallel()` as a default performance switch. First establish whether the work is CPU-bound, I/O-bound, ordered, and safe to run concurrently.

```java
Mono<OrderView> result = orderRepository.findById(orderId)
    .switchIfEmpty(Mono.defer(() -> Mono.error(new NotFoundException(orderId))))
    .flatMap(order -> pricingClient.quote(order.items())
        .map(quote -> OrderView.from(order, quote)))
    .timeout(Duration.ofSeconds(3))
    .onErrorMap(TimeoutException.class, ex -> new DependencyUnavailableException("pricing", ex));
```

## Controllers and streaming

- Return `Mono<T>` for one asynchronous response and `Flux<T>` for a stream. Use `Mono<ResponseEntity<T>>` when status, headers, and body depend on asynchronous work.
- Make empty results and errors explicit; do not turn an asynchronous failure into a null or an empty success accidentally.
- Use `Flux<ServerSentEvent<T>>` for SSE when event metadata, IDs, retry hints, or heartbeats matter. Define disconnect cleanup and make the stream finite or intentionally long-lived.
- For request streaming, accept a reactive body such as `Flux<PartEvent>` or `Flux<Payload>` only when the endpoint can process incrementally; avoid eagerly collecting unbounded input.
- Keep serialization and buffer limits explicit for large payloads. Prefer streaming or pagination over `collectList()` for unbounded data.

## WebClient

Configure and inject a reusable `WebClient` rather than constructing one per request. Set connection, response, and read/write timeouts at the appropriate client layer. Map status codes at the boundary and include safe request identifiers in logs.

```java
Mono<Profile> profile = webClient.get()
    .uri("/profiles/{id}", id)
    .retrieve()
    .onStatus(status -> status.value() == 404,
        response -> Mono.error(new ProfileNotFoundException(id)))
    .onStatus(HttpStatusCode::is5xxServerError,
        response -> response.createException()
            .map(ex -> new RemoteServiceException("profiles", ex)))
    .bodyToMono(Profile.class)
    .timeout(Duration.ofSeconds(2))
    .retryWhen(Retry.backoff(2, Duration.ofMillis(100))
        .filter(this::isTransient)
        .jitter(0.5));
```

Retry only failures that are safe to retry. Bound attempts and delay, add jitter for shared dependencies, and do not blindly retry non-idempotent writes. Avoid retrying a whole workflow when only one idempotent remote operation needs resilience.

## Backpressure and concurrency

Every producer/consumer boundary needs a capacity decision. Identify whether the producer can slow down; otherwise choose a bounded buffer, window, batch, drop policy, or fail-fast behavior. Never add an unbounded queue to make overload invisible.

- Bound `flatMap` concurrency and any prefetch that can amplify load.
- Use `limitRate`, `buffer`, `window`, or `onBackpressureBuffer` only with an explicit size and overflow policy.
- Use `concatMap` for ordered writes and `flatMapSequential` when work may overlap but output order must be preserved.
- Apply rate limits and bulkheads around downstream dependencies, not only at the HTTP edge.
- Test cancellation and slow subscribers, not only the happy path with a fast in-memory publisher.

## Context, security, and observability

Use Reactor `Context` for request-scoped correlation IDs, tenant data, and tracing metadata that must follow a subscription. Do not rely on a raw `ThreadLocal` or MDC surviving scheduler changes. If the application uses Micrometer context propagation, configure it deliberately and test the chosen mode.

Put `contextWrite` in the correct position: Reactor context flows from the subscriber toward upstream operators. Keep context keys typed or centrally defined. Never place credentials or large mutable objects in context.

Instrument subscription, success, error, cancellation, latency, retry count, queue depth, and downstream saturation. Avoid logging every element of a high-volume `Flux`; sample or aggregate instead. Use context-aware signal logging when correlation data is needed.

## Reactive data access and transactions

- Use reactive repositories and reactive transaction operators end-to-end when the application selects a reactive persistence stack.
- Do not mix JPA/JDBC calls into an R2DBC or WebFlux path without an explicit blocking boundary and capacity plan.
- Define transaction scope around the publisher and ensure the transaction is subscribed by the framework-owned request pipeline.
- Avoid `collectList()` or in-memory joins when the result can be paged, streamed, or joined by the database.
- Verify driver support and transaction semantics for the exact database; reactive APIs do not make a blocking driver non-blocking.

## Testing and verification

- Use `StepVerifier` for publisher behavior: values, completion, empty results, mapped errors, retry limits, timeout, and cancellation.
- Use `WebTestClient` for WebFlux HTTP contracts, including streaming and error responses.
- Use `TestPublisher` or controlled sinks for malformed, delayed, and misbehaving upstreams.
- Use `VirtualTimeScheduler` or `StepVerifier.withVirtualTime` for backoff and time-based operators; do not use `Thread.sleep` in tests.
- Add a blocking-call detector such as BlockHound when the project supports it, and treat violations as a design signal rather than suppressing them broadly.
- Verify with the project's formatter, compile/build, relevant tests, static analysis, and a diff review. For load-sensitive changes, record the concurrency, timeout, queue, and retry assumptions.

## Review checklist

Before finishing a reactive change, confirm:

- The API's `Mono`/`Flux` cardinality and streaming behavior are intentional.
- No blocking call, unmanaged subscription, or unbounded collection is hidden in the pipeline.
- Concurrency, backpressure, timeout, cancellation, and retry behavior have owners and limits.
- Error mapping preserves useful causes and produces the intended HTTP/domain response.
- Context, security metadata, tracing, and logging survive scheduler changes.
- Tests cover empty, error, timeout, retry exhaustion, slow consumer, and cancellation paths.

## References

- Spring WebFlux overview: https://docs.spring.io/spring-framework/reference/web/webflux/new-framework.html
- Spring WebClient: https://docs.spring.io/spring-framework/reference/web/webflux-webclient.html
- Reactor reference guide: https://projectreactor.io/docs/core/release/reference/
- Reactor retry and context guidance: https://projectreactor.io/docs/core/release/reference/faq.html
