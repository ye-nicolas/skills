# Java Implementation Plan Template

Use only sections that carry real information for the change.

```markdown
# <Change> implementation plan

## Scope and evidence

- Requested outcome:
- Non-goals:
- Repository evidence:
- Current behavior:
- Intended behavior:
- Contracts preserved:

## Decisions and assumptions

| Item | Status | Evidence or validation action |
|---|---|---|
| ... | decided / assumed / open | ... |

## Ordered implementation slices

### F01 — <Observable outcome>

- Objective:
- Files and symbols:
- Contract change:
- Contracts preserved:
- Implementation steps:
- Focused tests and expected red signal:
- Verification command and expected result:
- Dependencies:
- Risk and rollback:

## Cross-cutting changes

Include only applicable compatibility, migration, security, concurrency,
observability, build, documentation, rollout, and rollback work.

## Final verification

- Repository-required gate:
- Integration or manual evidence:
- Diff and scope review:
- Remaining verification gaps:
```

Every slice must leave the repository in a coherent state and have its own
completion evidence. Do not mark a plan or task complete before the stated
verification has actually passed.
