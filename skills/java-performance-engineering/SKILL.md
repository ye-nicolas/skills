---
name: java-performance-engineering
description: Diagnose and improve Java performance using measured workloads, profiling, benchmarks, and before/after evidence. Use for latency, throughput, CPU, allocation, garbage collection, memory, contention, startup, or resource-capacity work; do not optimize from code appearance or use microbenchmarks to claim whole-system performance.
---

# Java Performance Engineering

Improve a defined performance outcome without weakening correctness,
maintainability, overload behavior, or resource limits. Measure the actual
bottleneck first and preserve a reproducible baseline.

## Define the performance contract

Inspect the target JDK, runtime flags, deployment topology, workload, data size,
dependencies, and existing performance or capacity tests. Establish:

- the user- or operator-visible metric: latency percentile, throughput, startup,
  memory, allocation, CPU, pause time, queue depth, or resource saturation;
- the representative workload, concurrency, data distribution, warm-up,
  duration, and environment;
- the current baseline, target, measurement error, and correctness constraints;
  and
- the component and resource boundary that owns the result.

Do not turn a vague request such as “make it faster” into a guessed optimization.
If no target exists, establish a diagnostic baseline and label recommendations
as hypotheses.

## Select evidence appropriate to the claim

- Use application metrics and a representative load test for end-to-end latency,
  throughput, saturation, and overload behavior.
- Use JFR or an established profiler for CPU, allocation, locks, I/O, thread
  states, and garbage-collection evidence in a realistic run.
- Use heap histograms or dumps only when retention, leaks, or dominant live
  objects are in scope; handle dumps as potentially sensitive data.
- Use JMH for isolated JVM-level code claims that require warm-up, forks, and
  dead-code protection. Do not substitute a microbenchmark for database,
  network, framework, or whole-service behavior.
- Use generated SQL, query plans, broker/client metrics, or pool telemetry when
  an external resource is the likely bottleneck.

Prefer the repository's existing benchmark and load-test tooling. Do not add a
dependency or profiler agent merely because it is familiar.

## Optimization workflow

1. Reproduce the performance problem and capture a stable baseline.
2. Identify the limiting resource and the code or configuration path consuming
   it. Separate steady-state cost from startup, warm-up, spikes, and overload.
3. Form one falsifiable hypothesis and predict which metric should change.
4. Make the smallest coherent correction at the owning boundary.
5. Repeat the same measurement with equivalent inputs and environment. Report
   variance, not only the best run.
6. Run correctness, failure-path, and capacity verification. A faster result
   that drops work, changes ordering, increases timeouts, or hides rejection is
   not a valid improvement.
7. Inspect readability and operational cost before keeping the optimization.

## Java performance boundaries

- Distinguish CPU work, allocation pressure, retained memory, GC pauses, lock or
  monitor contention, thread scheduling, queueing, blocking I/O, and downstream
  saturation. Each requires different evidence and remedies.
- Check object lifetime and allocation rate before adding pooling or caches.
- Treat platform-thread pools, virtual threads, Reactor schedulers, and broker
  concurrency as workload and capacity choices, not universal speed switches.
- Preserve interruption, cancellation, backpressure, deadlines, and bounded
  overload behavior.
- Evaluate JVM flags only against the configured JDK and measured workload; do
  not copy a generic production flag set.

Use `$effective-java-concurrency` when task lifecycle or shared state determines
correctness, `$jpa-patterns` for query and connection behavior,
`$springboot-reactive-patterns` for reactive pipelines, and
`$spring-messaging-patterns` for consumer lag and broker capacity.

## Deliver the result

Report the workload and environment, baseline, evidence locating the bottleneck,
change or recommendation, before/after results with variance, correctness and
capacity checks, and remaining limits. For a review without measurements,
separate confirmed defects from measurement proposals and speculative risks.
