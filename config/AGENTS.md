# Global Working Agreements

Write code for the people who will read, debug, extend, and operate it later.
Correct behavior is necessary, but a change is not complete when its design is
needlessly difficult to understand.

## Scope and context

- Follow repository and directory-specific instructions over these global
  defaults.
- Inspect the relevant code, tests, configuration, and call sites before
  changing behavior. Do not infer a contract from a name alone.
- Make the smallest coherent change that satisfies the request. Do not mix in
  unrelated cleanup, speculative abstractions, dependency changes, or style
  rewrites.
- Keep one user-facing functional item in progress at a time. Parallelize
  independent investigation, implementation substeps, and verification when
  they support that item; do not start unrelated work.

## Human-maintainable code

- Prefer the simplest design that makes the current contract explicit. Reuse
  existing project patterns, language and runtime facilities, and framework
  capabilities before adding a helper or abstraction.
- Choose names that express domain intent. Avoid vague names, unexplained
  abbreviations, boolean parameters with unclear meaning, and comments that
  merely translate syntax into prose.
- Keep classes and methods cohesive and keep each block at a consistent level
  of abstraction. Extract code when the extracted concept has a meaningful
  name or independent contract, not to satisfy an arbitrary size limit.
- Make important states, invariants, ownership, side effects, failures, and
  lifecycle boundaries visible in types and APIs. Do not collapse materially
  different outcomes into `null`, `false`, or a generic exception.
- Prefer immutability and narrow visibility when they simplify reasoning.
  Avoid cleverness, premature optimization, and indirection that has no current
  caller or demonstrated variation.
- Comments and documentation should explain why a constraint, trade-off, or
  surprising decision exists. Keep externally visible contracts documented;
  let straightforward implementation explain itself.
- Preserve existing public behavior unless the request explicitly changes it.
  Update affected callers, tests, and contract documentation together.

## Tests and verification

- Test observable behavior and important failure paths. Prefer real values and
  small fakes; mock external or expensive boundaries when isolation is useful.
  Do not introduce an interface solely to make a test mockable.
- Discover and use the repository's existing formatter, build wrapper, static
  analysis, and test commands. Do not invent target names or assume every
  project uses Maven, Gradle, Make, or a particular plugin.
- Run verification proportional to the changed behavior and risk. Production
  code changes normally require relevant existing tests even when no test file
  changed.
- Treat completion as verified behavior, not written code. Report the commands
  that ran, their results, and any verification gap honestly.

## Shell commands

Use `rtk` for supported shell commands to keep output compact. Use
`rtk proxy <command>` or the unwrapped command when exact raw output or tool
compatibility is required. Do not let output filtering hide evidence needed to
diagnose a failure.

## Python tooling

- Prefer `uv` for Python environments, dependency operations, and one-off
  tools.
- Respect the project's existing package manager, manifest, lockfile, and
  documented commands. Use `uv sync`, `uv run`, and `uv add` when the project is
  already uv-managed; do not migrate a project from another workflow unless
  the user requests it.
- For temporary dependencies that should not modify project files, prefer
  `uv run --with <package> <command>` or `uvx <tool>` over plain
  `pip install`.
- Tool preference does not authorize adding or changing project dependencies.
  Use `pip` directly only when `uv` is unavailable or the established project
  workflow explicitly requires it.

## Conditional workflows

Read only the applicable workflow file next to this global `AGENTS.md`:

- A non-trivial change needs decomposition or several implementation steps:
  `PROJECT_EXECUTION.execution.md`
- The project root, setup, or verification entry points are not established:
  `PROJECT_EXECUTION.initialization.md`
- Verification is multi-step, cross-cutting, release-bound, or needs formal
  completion evidence: `PROJECT_EXECUTION.verification.md`
- Test-boundary, fixture, fake, stub, mock, database, or Spring Data projection
  decisions matter: `PROJECT_EXECUTION.test-doubles.md`
