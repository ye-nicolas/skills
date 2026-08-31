# Logging correlation context review

Read this reference only when a candidate involves a request-log object, correlation identifier, MDC, structured logging, or logging context that crosses an asynchronous boundary.

## Identify the responsibility before recommending MDC

Distinguish these concepts before judging the implementation:

- request identity covers one inbound HTTP request;
- method or operation identity covers one application use case and may come from a DTO or caller;
- distributed trace and span identities are owned by the tracing system;
- business correlation identity links work across requests, messages, retries, or jobs;
- a request-log or audit event records explicit data such as method, URL, outcome, duration, actor, or a sanitized payload.

MDC is a carrier for log-enrichment context, not a replacement for every field of a request-log or audit event. Keep transport responses, domain contracts, persisted audit records, and message headers explicit. Do not use one mutable field named `traceId` for several scopes.

## Reconstruct the logging lifecycle

For factories, `start` methods, filters, interceptors, and mutable log objects, trace representative callers and reconstruct:

1. context construction and default identifier generation;
2. caller-supplied context and its validation;
3. the first log statement or other observable sink;
4. later mutation, end logging, and failure paths.

A log statement observes the values available at that call. Mutating the object later does not rewrite the earlier log event.

Classify the writing as problematic when any of these are true:

- the first log has a generated identifier but the same field is later overwritten with a caller identifier;
- logs, responses, downstream calls, or persisted records that should correlate use different identities;
- validation or another failure can happen before required log context is installed;
- one identifier name conflates request, operation, distributed trace, or business-correlation scope;
- a mutable start object makes it unclear whether a log describes request start, request completion, or the final outcome.

Do not flag mutation by itself. It can be valid when every required field is finalized before the log call, or when separate start and end events intentionally carry phase-specific state and stable identifiers.

## Choose the representation by responsibility

- For request-wide log correlation, prefer a servlet filter or equivalent boundary that installs a stable request ID before downstream logging.
- For method or client-supplied operation identity, validate it and keep it as a separately named explicit field; add it to MDC only for the scope where it is meaningful.
- For distributed tracing, use the tracing system's trace and span context rather than generating an unrelated value with the same name.
- If a request-log object only exists to concatenate mutable data into ordinary log text, prefer parameterized structured start and completion events with explicit fields.
- If the object is an audit, persistence, or transport contract, keep a typed event or value object; MDC alone cannot preserve that contract.
- If duration and outcome are required, make start time and completion observation explicit instead of returning a mutable object that callers must finish correctly.

## Evaluate MDC implementation

When MDC is used, verify that:

- key names express scope, such as `requestId`, `operationId`, `traceId`, `spanId`, or `correlationId`;
- untrusted inbound values have an explicit trust policy and safe length and character constraints before entering logs;
- values are installed before the logs they must correlate and are echoed to a response only when that is part of the HTTP contract;
- nested scopes restore previous values and request or task cleanup occurs in `finally`;
- the configured encoder or pattern actually emits the selected MDC keys;
- executor, `CompletableFuture`, scheduler, reactive, virtual-thread, async-servlet, and message-listener boundaries deliberately propagate or rebuild context.

Recommend MDC only after confirming the logging framework and execution model. Route deeper context-propagation correctness to the concurrency or reactive skill, distributed tracing and operational design to the observability skill, and untrusted-identifier policy to the security skill.
