# Execution

Use this chapter only when you are decomposing and carrying out a functional
item.

Before implementation, understand the current contract and, when the change is
not trivial, decompose it into:

1. One functional item with a clear completion boundary.
2. The smallest ordered substeps needed to finish that item.
3. A concrete verification step that proves the item is complete.

For a small, obvious edit, a formal task breakdown is unnecessary. The behavior
to preserve or change and the verification boundary must still be clear.

Treat substeps as part of the same functional item. They are implementation
steps, not separate tasks, unless they each have an independent completion
boundary and independent verification.

## WIP 1

At any moment, allow only one functional item to be in progress. Read-only
investigation and verification may cover several files or layers when they all
support that same item.

While implementing a functional item, do not quietly start additional
unrelated items or "just in case" refactors.

## Implementation discipline

- Trace callers and externally visible behavior before changing a contract.
- Prefer existing project patterns and standard/framework capabilities over a
  new abstraction.
- Keep the diff focused, but include every directly affected caller, test, and
  contract document required for consistency.
- If adjacent code is confusing but does not block the requested change, leave
  it unchanged and report it separately.
