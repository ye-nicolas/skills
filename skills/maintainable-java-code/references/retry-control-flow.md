# Retry Control Flow

Read this reference only when an operation can make more than one attempt or
when retry exhaustion changes its observable result.

## Establish the retry contract

Identify the owner of the retry policy and confirm:

- which failures are retryable and which propagate immediately;
- whether the configured limit counts attempts or retries;
- the backoff, timeout, cancellation, and interruption behavior; and
- whether work performed before a failure is safe to repeat.

Preserve the existing classification and limits unless the request changes the
policy. Use `$effective-java-concurrency` when shared state, task lifecycle,
interrupt handling, executor ownership, or memory visibility determines
correctness. Use the relevant framework skill when it owns the retry mechanism.

## Keep terminal paths direct

Make the loop or retry composition show the meaningful paths where they occur:

```text
success                         -> return
retryable failure below limit   -> next attempt
retry limit reached             -> terminal failure
non-retryable failure           -> propagate immediately
cancellation or interruption    -> follow the owning contract
```

Do not leave an unreachable exception after a loop whose paths already return
or fail. Do not catch a broad exception merely to classify it as retryable. When
an attempt can perform an external effect before failing, verify idempotency,
deduplication, or compensation before allowing another attempt.

## Validation questions

- Can a reader tell why another attempt occurs?
- Is the maximum number of attempts unambiguous?
- Are exhaustion, non-retryable failure, cancellation, and interruption
  distinguishable where the contract requires it?
- Are repeated state changes or external effects safe and covered by focused
  tests?
