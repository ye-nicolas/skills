# Executors and Virtual Threads

Use the runtime and framework's managed executor when it already owns task
lifecycle. Create an executor only when the component has a distinct capacity,
threading, or shutdown contract, and close only executors it owns.

## Choose the execution model

Classify the work before choosing an executor:

- CPU-bound work needs bounded parallelism near measured CPU capacity.
- Blocking I/O on platform threads needs a bounded concurrency and queue policy
  derived from downstream capacity and latency goals.
- Virtual threads suit large numbers of mostly waiting tasks on a supported JDK.
  They improve scalability of blocking code, not the latency of one operation,
  and do not remove database, HTTP, memory, or rate limits.
- Reactor, event loops, and framework-managed async models have their own
  scheduling contracts. Do not add an unrelated pool without tracing the
  boundary and context propagation.

Do not migrate execution models for style. State the expected benefit and
measure the relevant workload.

## Platform-thread pools

For a custom `ThreadPoolExecutor`, choose and document:

- core and maximum workers;
- queue type and explicit capacity;
- thread names and daemon policy;
- rejection behavior visible to the submitter;
- context capture/cleanup;
- metrics and overload response;
- creator and shutdown owner.

An unbounded queue can turn overload into memory growth and stale work. With an
unbounded queue, `maximumPoolSize` above the core size normally does not absorb
bursts because tasks continue to enqueue. A bounded queue makes overload
explicit but requires an API-level rejection contract.

Use a named `ThreadFactory` for owned platform threads when the target JDK
supports the chosen API. Select daemon status deliberately: daemon workers may
be terminated without completing cleanup when all non-daemon threads exit.

## Rejection policies

- `AbortPolicy` is a clear fail-fast choice when the caller maps
  `RejectedExecutionException` to an overload result and records it.
- `CallerRunsPolicy` can slow a suitable submitter, but is unsafe for event-loop
  threads, latency-sensitive callers, submission under a lock, or work that is
  invalid on the caller thread. After shutdown it may discard work.
- Discard policies are appropriate only for an explicitly lossy contract.
  Caller-visible futures for discarded work must not remain incomplete.

Rejection may occur synchronously before a `Future` or `CompletionStage` is
returned. Preserve the established API contract unless the change explicitly
redefines how failure is delivered.

## Capacity and sizing

Treat formulas as starting hypotheses, not configuration defaults. For a
platform-thread workload with measured wait time `W`, compute time `C`, target
CPU utilization `U`, and available processors `N`, a common estimate is:

```text
threads ≈ N * U * (1 + W / C)
```

Measure `W` and `C` after execution begins; executor queue wait is an outcome of
the current configuration, not intrinsic workload wait. Bound the result by
downstream capacity and validate queue wait, latency distribution, throughput,
timeouts, and rejection under representative bursts.

Choose queue capacity from the acceptable queue wait and measured service rate,
then round conservatively and load test. A larger pool or queue may only move
contention and cause more work to finish after callers time out.

## Virtual threads

On a supported JDK, create one virtual thread per blocking task rather than a
pool of reusable virtual-thread workers. A per-task executor is a submission and
lifecycle abstraction, not a downstream capacity limiter.

```java
ThreadFactory factory = Thread.ofVirtual()
    .name("request-", 0)
    .factory();
ExecutorService executor = Executors.newThreadPerTaskExecutor(factory);
```

Create the executor at the owning component/application boundary, not for each
task. If thread names are unnecessary, use the JDK's virtual-thread-per-task
factory available to the target version.

Do not pool virtual threads or apply the platform-thread `W/C` formula to them.
Limit scarce downstream resources with an existing connection pool, rate
limiter, semaphore, or admission control only when its ownership and overload
contract are clear. Do not add a duplicate limiter without a separate capacity
reason.

Avoid per-thread caches of expensive objects when virtual-thread count may be
large. Request context in thread locals still requires explicit lifecycle and
cleanup. Check the target JDK for pinning behavior and use JFR or thread dumps
when it matters; do not repeat obsolete pinning advice across JDK versions.

## Shutdown

Use the repository/framework lifecycle helper when its contract fits. Otherwise
follow the JDK two-phase pattern for an owned executor:

1. `shutdown()` to reject new work.
2. Bounded `awaitTermination()` for graceful completion.
3. `shutdownNow()` when the graceful deadline expires.
4. Handle queued tasks returned by `shutdownNow()` and verify termination when
   the lifecycle contract requires it.

Restore interrupt status when the API boundary cannot propagate
`InterruptedException`. If a removed queued task corresponds to a future visible
to a caller, cancel or otherwise complete it so `get()` cannot wait forever.

## Verification

Exercise steady state, saturation, synchronous rejection, task failure,
cancellation, interruption, context cleanup, graceful shutdown, and forced
shutdown. Measure queue wait, active workers, downstream utilization, timeouts,
and rejections. For virtual threads, inspect resource pressure rather than
counting threads as a defect by itself.

## Primary references

- [ExecutorService](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ExecutorService.html)
- [ThreadPoolExecutor](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ThreadPoolExecutor.html)
- [Oracle virtual threads guide](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html)
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
- [JEP 491: Synchronize Virtual Threads without Pinning](https://openjdk.org/jeps/491)
