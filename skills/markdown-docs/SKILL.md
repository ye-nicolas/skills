---
name: markdown-docs
description: Convert Java, Spring Boot, or other source code, tests, configuration, APIs, and repository structure into accurate Markdown documentation. Use when generating or updating README files, API documentation, architecture notes, ADRs, runbooks, tutorials, code explanations, migration guides, or changelogs from an implementation; treat source code as the authority and label inferences. Do not use for Word, PDF, slide, or spreadsheet artifacts.
---

# Code-to-Markdown Documentation

Convert an implementation into Markdown that a maintainer, developer, operator, or reviewer can use without reconstructing the codebase. The implementation is the primary source of truth; the user's idea supplies the documentation goal, audience, and scope but does not override observed behavior.

## Workflow

1. Identify the audience, purpose, repository or module scope, and requested output path. If the user names a file, preserve it; otherwise choose a conventional path such as `README.md`, `docs/api/title.md`, `docs/adr/NNNN-title.md`, `docs/design/title.md`, or `docs/runbooks/title.md`.
2. Inspect the implementation before drafting. Start from the public entry point and follow the relevant flow through controllers or commands, services, repositories or clients, persistence, events, configuration, and error handling. Read the build files, tests, examples, and existing docs that define the behavior.
3. Create a compact evidence map while reading:
   - **Symbol or behavior**: the API, class, route, setting, workflow, or error being documented.
   - **Source**: the file and symbol, test, configuration key, or command that proves it.
   - **Observed behavior**: what the code actually does, including defaults and limits.
   - **Gap**: missing coverage, ambiguity, or conflict between code and tests.
4. Classify the document before writing:
   - **README**: what it is, prerequisites, setup, usage, configuration, tests, and links.
   - **ADR**: context, decision, alternatives, consequences, and status.
   - **API documentation**: endpoints or public methods, inputs, outputs, errors, authentication, examples, and compatibility notes.
   - **Design document**: problem, goals, non-goals, constraints, proposed design, data/control flow, risks, rollout, and validation.
   - **Runbook**: symptoms, prerequisites, diagnosis, safe actions, rollback, escalation, and verification.
   - **Tutorial or code explanation**: learning goal, prerequisites, progressive steps, complete examples, expected output, and troubleshooting.
   - **Changelog or migration guide**: affected versions, user-visible changes, upgrade steps, breaking changes, and rollback considerations.
5. Separate facts from interpretation:
   - **Observed**: directly supported by source, tests, configuration, command output, or user-provided material.
   - **Inferred**: a reasonable explanation derived from evidence; label it when it affects a decision.
   - **Proposed**: future behavior or a recommendation; label it as proposed and include acceptance or validation criteria.
   - **Unknown**: missing information; use `TODO`, an open question, or a clearly marked assumption instead of inventing a value.
6. Draft the smallest complete structure for the document type. Keep sections in the order a reader needs them: purpose and scope, prerequisites or context, behavior or procedure, examples, verification, and limitations or next steps.
7. Validate the result against the source. Check commands, paths, symbols, links, configuration keys, code examples, version claims, and expected outputs. Remove unsupported claims and stale instructions.
8. If editing an existing Markdown file, preserve useful structure and links, update affected sections, avoid duplicating information, and keep the diff focused. Do not rewrite unrelated prose solely for style.

## Markdown conventions

- Use one level-one heading per file and ATX headings (`##`, `###`) below it.
- Start with a short summary and state the scope or audience when the file is not self-explanatory.
- Use fenced code blocks with a language identifier: `java`, `bash`, `json`, `yaml`, `http`, or the closest accurate language.
- Show commands exactly as they should be run. Explain placeholders and identify commands that are destructive, environment-specific, or require credentials.
- Prefer bullets for short independent facts, numbered steps for procedures, and tables only for compact field or option comparisons.
- Use relative Markdown links for repository files. Link to a symbol or section when it materially improves navigation; do not create links to files that were not verified.
- Use Mermaid only when a flow, sequence, dependency, or state transition is materially clearer as a diagram. Keep the adjacent prose understandable without rendering Mermaid.
- Keep examples minimal but executable when possible. Mark pseudocode and incomplete snippets explicitly.
- Avoid duplicating source code wholesale. Explain the contract and show the smallest excerpt that proves the behavior.
- Keep secrets, tokens, private URLs, and personal data out of examples. Replace them with safe placeholders.

## Implementation-to-documentation rules

When the source is Java, Spring Boot, or another codebase:

- Document behavior at the public boundary first: purpose, inputs, outputs, side effects, error behavior, lifecycle, and concurrency or blocking assumptions.
- Trace important flows through controller or entry point, service, repository or client, persistence, events, and error handling. Do not document only class names.
- Derive configuration from actual configuration files, binding classes, defaults, and startup code. Distinguish required settings from optional defaults.
- Derive API examples from routes, request/response types, validation annotations, serializers, and tests. Mention status codes and error payloads only when supported.
- For reactive code, document `Mono`/`Flux` cardinality, streaming behavior, cancellation, backpressure, timeouts, retries, and any blocking boundary. Use `$springboot-reactive-patterns` for design review and correctness guidance.
- For Spring MVC or blocking Java code, document transactions, pagination, caching, async behavior, and operational limits when the code establishes them. Use `$springboot-patterns`, `$jpa-patterns`, or `$effective-java-concurrency` as companions when needed.
- Treat tests as executable evidence of intended behavior, but call out gaps when implementation and tests disagree or important paths are untested.
- If the input is only a code snippet, document the behavior visible in that snippet and list the integration context that cannot be verified. Do not turn a class name, dependency, annotation, or TODO into a claim about a working feature.
- If the code has generated sources, framework conventions, reflection, annotations, or external configuration, identify the mechanism and inspect the relevant generated or bound behavior before documenting it.

## Handling the user's idea

Use the idea only to determine what the documentation should explain:

- Preserve the requested audience, purpose, and terminology.
- Map the idea to the actual implementation, then explicitly show where they differ.
- Put unsupported desired behavior under `Proposed`, `Planned`, or `Open questions`; never present it as current behavior.
- If no implementation is available, stop at a clearly labeled specification or design draft rather than pretending to document existing code.

## Common output skeletons

### README

```markdown
# Project name

Short description and supported scope.

## Prerequisites
## Quick start
## Usage
## Configuration
## Development and tests
## Deployment or operations
## Troubleshooting
## Contributing
```

### ADR

```markdown
# ADR-NNNN: Decision title

- Status: Proposed | Accepted | Superseded | Deprecated
- Date: YYYY-MM-DD

## Context
## Decision
## Alternatives considered
## Consequences
## Validation and follow-up
```

### Design document

```markdown
# Design title

## Summary
## Problem
## Goals
## Non-goals
## Constraints and assumptions
## Proposed design
## Data and control flow
## Failure modes and observability
## Rollout and rollback
## Validation plan
## Open questions
```

## Completion checklist

Before delivering Markdown, confirm:

- The document type, audience, scope, and output path are clear.
- The implementation source, tests, configuration, or command output supporting each important claim is known.
- Statements are supported by source material or marked as inferred, proposed, assumed, or unknown.
- Code, commands, configuration, paths, links, and examples match the inspected project.
- Setup and operational instructions include prerequisites, safety notes, and verification.
- The document explains errors, limitations, compatibility, and next steps when relevant.
- Existing Markdown structure and links were preserved unless a change was necessary.
- The final file is valid Markdown and contains no accidental secrets or placeholder text that was not intentional.
