# Stateful Workflows

Read this reference only when a Java application flow creates, compares, or
changes stored state and the distinction between states affects behavior.

## Model meaningful distinctions

Start from the existing domain contract. Identify which states cause callers to
take different actions or cause the system to perform different side effects.
Represent those states distinctly when collapsing them would hide behavior.

For a compare-and-apply flow, possible distinctions include applied, unchanged,
stale, rejected, or conflicting. These are examples, not required names or a
required enum. Reuse the project's existing result model when it already
expresses the contract.

At the call site, make each meaningful result's consequences visible:

- whether state is written;
- whether history or an outbox record is created;
- whether an event, message, or notification is published; and
- whether the operation returns normally or fails.

An unchanged result is not automatically success or failure. Preserve the
existing rule for drift repair, duplicate suppression, or conflict reporting.

## Distinguish creation from comparison when behavior differs

Treat absent or initial state separately from existing-state comparison when
they have different validation, construction, persistence, or publication
semantics. Separate methods can help when their names reveal those differences,
but do not split them mechanically when one cohesive flow is clearer.

When constructing new state, make required identity, domain values, timestamps,
flags, and defaults visible at the construction boundary. Verify generated
builders or factories before assuming field initializers supply required
defaults, and inspect other construction sites before changing that contract.

Avoid a generic callback or helper that forces initial, unchanged, stale,
conflicting, and applied behavior through one abstraction if doing so hides
which state changes or side effects occur.

## Validation questions

- Can a reader distinguish initial state from every existing-state outcome?
- Does every meaningful outcome map visibly to its writes and external effects?
- Are important defaults established exactly once at construction?
- Do focused tests cover the state distinctions that callers or side effects
  depend on?
