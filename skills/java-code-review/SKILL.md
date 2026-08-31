---
name: java-code-review
description: Review Java and Spring change sets against their requirements and repository contracts, reporting evidence-backed correctness, regression, test, security, performance, and maintainability findings. Use for diffs, pull requests, staged or working-tree changes, and pre-merge review. Do not implement fixes unless the user separately authorizes changes or replace a focused architecture or security audit.
---

# Java Change Review

Determine whether a Java or Spring change satisfies its intended contract
without introducing defects or unjustified complexity. Review the change set in
repository context and report only actionable findings supported by a concrete
trigger and impact. Review is read-only unless the user also asks for fixes.

## Establish the review contract

Identify the requested change, relevant specification or plan, repository
instructions, comparison base and head, changed files, supported JDK/framework
versions, and verification already performed. If the user supplies a pull
request or commit range, review that exact range. Otherwise inspect the staged
or working-tree change they placed in scope; do not silently review the entire
repository.

Start with the diff summary and changed-file list, then read the complete patch
when practical. Trace changed public behavior through important callers,
tests, configuration, schemas, migrations, generated behavior, and error
mapping. A nearby search match, suspicious name, or generic best practice is a
lead, not a finding.

## Review in impact order

1. **Requirement compliance** — missing acceptance criteria, unintended scope,
   incompatible behavior, or a change that solves a different problem.
2. **Correctness and failure behavior** — validation, absence, state changes,
   side-effect order, transactions, exceptions, retry, cancellation, resource
   ownership, and partial failure.
3. **Compatibility and integration** — Java API, serialization, HTTP/message
   contract, database schema, configuration, dependency, supported JDK, and
   rollout ordering.
4. **Tests and verification** — meaningful changed outcomes without coverage,
   a test boundary that mocks away the claim, nondeterminism, or missing
   repository-required evidence.
5. **Security, performance, and operations** — only when a concrete trust,
   resource, latency, capacity, telemetry, or production failure boundary is
   affected.
6. **Maintainability** — hidden states, misleading names, tangled
   responsibilities, or accidental complexity likely to make the changed
   behavior unsafe to extend.

Load one focused companion when a material boundary needs specialist
interpretation: `$effective-java-core`, `$effective-java-concurrency`,
`$springboot-patterns`, `$springboot-reactive-patterns`, `$jpa-patterns`,
`$spring-messaging-patterns`, `$springboot-security`,
`$java-performance-engineering`, or `$java-build-dependency-management`.
Do not activate every specialist because its dependency appears in the build.
Use `$java-architecture-review` instead when the primary question is module,
service, ownership, or dependency structure.

## Calibrate findings

Read [finding calibration](references/finding-calibration.md) before producing
inline review findings. Every finding must include:

- a narrow changed-code location;
- the input, state, interleaving, deployment, or caller that triggers it;
- expected versus actual behavior and the violated contract;
- concrete user, data, security, operational, or maintenance impact;
- the smallest coherent remedy; and
- a focused test or check that would prove the remedy.

Downgrade confidence or report a verification gap when the trigger depends on
unavailable runtime, data, configuration, or external service evidence. Do not
inflate severity because an issue is easy to imagine, report unrelated
pre-existing defects as caused by the change, or manufacture style findings
when the code is clear.

## Review feedback and delivery

List findings first in severity order. Keep summaries short and place strengths
or general observations after actionable findings. When no actionable finding
is established, say so and state the files, contracts, and verification limits
reviewed; absence of findings is not proof that unrun integration behavior
passes.

If the user also requested fixes, finish the review before changing code, then
handle one accepted finding at a time through the owning implementation skill
and `$java-verification`. Verify external reviewer suggestions against the
repository before implementing them. Do not dispatch another reviewer, publish
comments, approve a pull request, or mutate GitHub state unless the user asks
and the required capability is available.
