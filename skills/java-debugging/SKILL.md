---
name: java-debugging
description: Diagnose concrete Java or Spring failures by reproducing the symptom, tracing the failing path, testing evidence-backed hypotheses, and identifying the root cause. Use for exceptions, wrong results, startup failures, flaky behavior, hangs, leaks, or regressions; do not implement a fix unless the user also asks for one.
---

# Java Debugging

Determine why an observed Java or Spring failure occurs. Separate the symptom,
trigger, root cause, and contributing conditions, and stop at diagnosis when the
user has not authorized a code change.

## Establish the failure contract

Before forming a theory, inspect repository instructions, the configured JDK
and framework versions, the failing entry point, relevant callers, tests,
configuration, data assumptions, and the complete error or incorrect result.

Record:

- expected behavior and the evidence defining it;
- actual behavior, first known occurrence, and reliable trigger;
- last known working revision or environment and relevant recent changes when
  that evidence exists;
- environment, input, state, timing, and concurrency conditions;
- whether the failure is deterministic, intermittent, or load-dependent; and
- the smallest practical command or scenario that reproduces it.

Do not infer the root cause from an exception's final line, a log search match,
or the name of a failing method.

## Evidence-first workflow

1. Reproduce the exact symptom when the environment permits it. If it cannot be
   reproduced, preserve that as a verification gap rather than changing code to
   manufacture a passing result.
2. Compare relevant recent changes, configuration, dependencies, data, and a
   similar working path when available. Treat differences as hypotheses, not
   causes, until the failure mechanism connects them to the symptom.
3. Trace backward from the first incorrect observable state or earliest useful
   exception frame through validation, control flow, state changes, external
   calls, transactions, and asynchronous boundaries.
4. Classify the likely boundary: contract or logic, configuration or wiring,
   data or persistence, dependency or protocol, concurrency or lifecycle,
   resource exhaustion, or environment/toolchain.
5. Rank a small set of hypotheses by how well each explains all known evidence.
   State what observation would confirm or reject each one.
6. Gather the narrowest additional evidence needed: a focused failing test,
   safe temporary diagnostic, debugger inspection, thread dump, JFR recording,
   generated SQL, dependency graph, or configuration comparison.
7. Identify the causal chain and distinguish the root cause from secondary
   failures, cleanup errors, retries, or misleading wrapper exceptions.
8. Define the smallest verification that would prove a proposed fix without
   implementing it unless requested.

## Java and Spring evidence

- Read the full exception chain, including suppressed exceptions, and preserve
  the earliest application frame with useful context.
- Check classpath, module, bytecode, and JDK compatibility for linkage or
  startup failures before changing application logic.
- For Spring, inspect the actual bean graph, profiles, condition reports,
  proxying, filter chain, transaction boundary, exception mapping, and bound
  configuration involved in the path.
- For JPA, distinguish application validation, flush/commit failures, database
  constraints, lazy access, locking, and transaction rollback.
- For concurrency, identify the invariant, ownership, happens-before or
  capacity contract, triggering interleaving, cancellation, interruption, and
  shutdown behavior. Use `$effective-java-concurrency` for corrective design.
- For reactive paths, trace subscription, empty/error signals, scheduler
  boundaries, cancellation, retry, and blocking calls. Use
  `$springboot-reactive-patterns` for corrective design.

Avoid broad debug logging that exposes secrets or personal data. Remove or
clearly identify temporary diagnostics before handing off an implementation.

## Diagnose without guessing

- Do not list generic possibilities as if they were findings.
- Do not call correlation causation; compare timelines and state transitions.
- Do not fix unrelated warnings while isolating the failure.
- Do not treat a retry, restart, larger timeout, cache clear, or added
  synchronization as a root-cause fix without evidence.
- Distinguish an existing environmental failure from a regression introduced by
  the change under review.

## Deliver the diagnosis

Report:

1. **Symptom and reproduction** — expected versus actual behavior and the
   smallest reliable trigger.
2. **Evidence** — relevant code path, data/configuration state, command output,
   and observations.
3. **Root cause** — the causal mechanism, not only the failing line.
4. **Impact and conditions** — affected callers, environments, inputs, timing,
   and side effects.
5. **Smallest remedy** — one recommended correction and material alternatives,
   routed to the appropriate implementation skill.
6. **Verification** — the focused regression test or observable check that
   would prove the remedy, plus any remaining uncertainty.

If the evidence does not establish a root cause, say `not yet determined`, list
the strongest remaining hypotheses, and request only the missing evidence that
would materially distinguish them.

When the user also authorized a fix and the root cause is established, hand off
to `$java-junit` or `$springboot-testing` for a failing regression test when
practical, then the domain skill that owns the correction and
`$java-verification` for fresh completion evidence. Do not blur an unconfirmed
hypothesis into an implementation task.
