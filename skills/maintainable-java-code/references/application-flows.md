# Readable Application Flows

Read this reference only when Java code coordinates meaningful business
decisions, state changes, or external effects.

## Outline the contract

Form a compact working outline of what must be true, what is read and validated,
which outcomes callers distinguish, what state changes, what is published, and
how each path terminates. This is a reasoning aid rather than a mandatory
user-facing deliverable. Verify it from code, callers, tests, configuration, and
collaborators instead of inferring the contract from names alone.

## Keep decisions and effects visible

- Keep the orchestration method at the business level. Move lower-level
  mechanics behind a domain-named boundary only when it reduces the reader's
  reasoning cost; do not extract methods mechanically.
- Make genuine execution prerequisites visible in the owning constructor,
  method signature, or public boundary. Express genuine optionality in the
  type, name, and contract instead of an unexplained `null` or fallback.
- Use a distinct result representation when callers need different follow-up
  actions for materially different outcomes. Keep a boolean, nullable value, or
  exception when it accurately expresses the established contract.
- At each decision, make the resulting state change, external effect, normal
  return, or failure visible at the responsible layer. Keep irreversible effects
  after the validations that own their prerequisites unless the contract
  intentionally requires another order.
- Do not remove a public overload, compatibility path, or supported fallback
  solely to make the design cleaner. If removal changes a caller or failure
  behavior, treat it as an explicit contract change and update affected callers
  and tests together.

## Load narrower guidance only when needed

When absent, initial, existing, unchanged, stale, or conflicting state changes
the flow, read [stateful-workflows.md](stateful-workflows.md). When multiple
attempts, retry classification, or retry exhaustion are in scope, read
[retry-control-flow.md](retry-control-flow.md). Read only the reference that
matches the actual code path.
