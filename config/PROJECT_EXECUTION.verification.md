# Verification

Use this chapter only when you need completion evidence, task-status wording,
or command rules.

## Explicit Completion Evidence

Treat completion as "the behavior has been verified", not "the code has been
written".

For each task or functional item, define:

1. What behavior counts as done.
2. The exact verification command, manual check, or observable result that
   proves it.
3. The expected outcome of that verification.

If a task list is being maintained, each entry should include its verification
evidence and current status, for example:

```text
F01: User registration
  Verification: curl -X POST /api/register -d '{"email":"test@example.com","password":"test-only-placeholder"}' | jq -e '.status == 201'
  Status: passing
```

## Discover the project entry points

Inspect repository instructions and build files before choosing commands. Use
the project's wrapper and established entry point, which may be a Makefile,
Maven or Gradle wrapper, package script, task runner, or CI-equivalent command.
Do not guess target or plugin names.

When a Makefile is the documented entry point, read it and use the matching
target. For example:

```bash
rtk make
```

For named tasks, use an existing target such as `rtk make format` or
`rtk make build`; these names are examples, not defaults.

## Format and static analysis

Run the repository's configured formatter on changed files or through its
normal project command. Prefer a check mode when the task is review-only. Do
not introduce a formatter or rewrite unrelated files solely to finish a small
change.

Run configured static analysis that is relevant to the change. Do not invoke
unconfigured Maven/Gradle goals merely because they are common elsewhere.

## Compile and Test

Build or compile every changed production path when the project provides a
practical command. Use the project's wrapper, for example:

```bash
rtk ./mvnw -DskipTests compile
```

Run the smallest relevant tests that exercise changed behavior, including
existing tests when production code changed. Expand to broader module or full
suite verification when the change is cross-cutting, high-risk, release-bound,
or the user requests it. A test-file diff is not the only reason to run tests.

Use repository coverage thresholds when configured. Treat coverage as a signal
for missing behavior, not a universal percentage target.

If a build or test fails because of a likely permission, network, Docker, or
sandbox restriction, retry only through the environment's normal approval path
and only when that evidence is necessary. Do not change production code to work
around a local test-environment limitation.

## Completion report

Report:

1. Formatter/static checks run and their results.
2. Build/compile command and result.
3. Focused and broader tests run and their results.
4. Any skipped check, environmental failure, or unverified behavior.
5. A focused diff review confirming no unrelated changes were introduced.

Do not substitute a successful compile for a failed behavioral test without
clearly stating the remaining gap.
