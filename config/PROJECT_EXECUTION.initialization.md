# Initialization

Use this chapter when a project has not yet established its root, setup, or
verification commands. Do not repeat it for a small follow-up in an already
understood project.

Establish enough of the operating contract to work safely. Do not turn
initialization into a separate deliverable when the required context is already
obvious.

## Startup Contract

The initialization phase must establish:

1. The project root and relevant module.
2. The expected setup, build, formatter, static-analysis, and test entry points.
3. One inexpensive baseline command that demonstrates the environment works,
   when running it is safe and useful.
4. A task or progress record only when the work is long-running or spans
   sessions.

## Project Root

If the active project directory is not obvious, identify it during
initialization before doing any feature work. Prefer repository markers such as
`git` root, `Makefile`, package manifests, or other project entry files. Do not
guess the folder when the workspace contains multiple candidates.

The exact project directory or workspace root the agent should treat as the
active working area must be clear before feature work starts.

## Report Placement

When a task produces report-style files, analysis notes, handoff records, or
other durable written outputs, place them under the active project directory or
workspace root established for the task. Do not default to global Codex folders,
date-stamped external workspaces, or other locations outside the current
project.

If the project already has a relevant docs, reports, or work/current directory,
use that existing structure. Otherwise, create the smallest clear project-local
path, such as `reports/` or `docs/reports/`, based on the project's conventions.

## Boundary

Stop initialization as soon as the current change can be implemented and
verified without guessing. Continue into the requested work in the same turn
unless the environment is genuinely blocked.
