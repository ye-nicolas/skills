# Java/Spring Observability Review Lens

Use this reference when the repository contains Java, Spring Boot, Spring MVC,
WebFlux, Spring Data, or Spring messaging code. The goal is to discover gaps in
the existing system, not to assume that every signal must be added.

## 1. Inventory the instrumentation surface

Inspect the build and runtime configuration for:

- Spring Boot Actuator and the exposed health, metrics, and Prometheus endpoints
- Micrometer registries, OpenTelemetry SDK or Java agent, exporters, and Collector configuration
- Logging implementation and appenders, including structured JSON configuration
- HTTP entry points: MVC controllers, filters/interceptors, WebFlux routes, and error handlers
- Outbound HTTP clients: `RestClient`, `WebClient`, `RestTemplate`, Feign, or other clients
- Persistence: JDBC, HikariCP, JPA/Hibernate, R2DBC, MongoDB, Redis, and cache layers
- Messaging: Kafka, RabbitMQ, JMS, SQS, Spring application events, retry, and dead-letter paths
- Asynchronous execution: `@Async`, schedulers, task executors, virtual threads, and batch jobs
- Deployment configuration: Docker, Kubernetes, probes, environment variables, OTLP endpoints,
  scrape configuration, and service version metadata

Use repository evidence such as `pom.xml`, `build.gradle`, `application*.yml`,
logging configuration, Docker/Kubernetes manifests, and the relevant code paths.

## 2. Check the signals by purpose

For each critical journey, determine whether the existing telemetry can:

- **Detect** — request rate, error rate, latency distribution, saturation,
  availability, queue lag, and business outcome where appropriate
- **Localize** — service, endpoint, dependency, database, consumer, executor,
  or instance causing the problem
- **Explain** — structured error details, exception type, retry attempt,
  dependency result, and trace/log context without leaking sensitive data

Credit existing Actuator, Micrometer, auto-instrumentation, dashboards, and
alerts. Report a gap only when the available signal cannot answer a concrete
failure question.

## 3. Java/Spring checks that commonly reveal gaps

- HTTP metrics use route templates rather than raw URLs or unbounded IDs.
- Trace context survives inbound HTTP, outbound HTTP, database calls, messaging,
  retries, scheduled work, and asynchronous executor boundaries.
- Logs include compatible `trace_id`/`span_id` correlation fields and preserve
  the original exception and operation context.
- Instrumentation is not duplicated by combining a Java agent with manual
  instrumentation or framework instrumentation without a deliberate reason.
- Database and connection-pool visibility covers query/operation latency,
  errors, pool exhaustion, and timeout paths without capturing sensitive query
  parameters by default.
- Messaging visibility covers publish/consume failures, processing latency,
  consumer lag, retry counts, and dead-letter outcomes.
- JVM and runtime signals cover heap, GC, thread/executor saturation, blocked
  tasks, CPU, and startup/readiness failures where they affect service health.
- Sampling, metric labels, log volume, retention, and exporter batching have an
  explicit cost and failure policy.
- Health/readiness probes reflect actual dependency readiness and are not used as
  a substitute for user-facing SLO monitoring.
- Telemetry export failure is observable; an application must not silently look
  healthy merely because its monitoring pipeline is broken.

## 4. Verification questions

For every proposed gap, state how it can be verified:

1. Exercise a representative success and failure path.
2. Confirm the expected metric, log, or trace exists.
3. Confirm the trace crosses the relevant service/dependency boundary.
4. Confirm the signal has bounded dimensions and no secret or unnecessary PII.
5. Confirm the dashboard and alert can detect the named failure and point to the
   next diagnostic signal.

If live telemetry or production configuration is unavailable, label the finding
as MED/LOW confidence and state exactly what must be checked later.
