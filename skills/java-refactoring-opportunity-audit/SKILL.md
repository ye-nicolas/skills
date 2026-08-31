---
name: java-refactoring-opportunity-audit
description: Audit an existing Java repository end to end to discover and prioritize coding-level improvement candidates in both duplicated and unique code. Use for explicit whole-codebase maintainability or modernization audits, similar-method inventories, and repository-wide functional-interface opportunity analysis. Do not use for one file or diff, a known refactor, debugging, or focused architecture, security, concurrency, persistence, or performance work.
---

# Java Codebase Improvement Audit

Discover and triage repository-wide code improvements without mistaking syntax similarity, novelty, or shorter code for better design. Cover repeated patterns and important one-off problems.

## Keep the role narrow

This skill owns broad discovery, initial contract validation, prioritization, and routing. It does not own implementation or deep specialist review. Flag architecture, security, concurrency, persistence, reactive, messaging, or measured-performance concerns and use an available focused skill when deeper analysis is required.

Do not change code unless the user separately asks for implementation. Do not let the breadth of the scan turn into unrelated cleanup recommendations.

## Audit the repository

Read repository instructions, build configuration, source roots, module boundaries, and the configured JDK. Treat an explicit whole-project request as a whole-source audit unless the user narrows it.

Read [references/audit-workflow.md](references/audit-workflow.md), then run [scripts/scan_java_refactoring_candidates.py](scripts/scan_java_refactoring_candidates.py) near the start unless the repository is too small to benefit. Treat its output as a candidate index, not as findings.

Expand from mechanical signals into high-fan-in, large, business-critical, or boundary code even when it is unique. Never present a mechanical screen or sample as complete semantic coverage.

## Validate and classify

Inspect representative implementations, important callers, tests, and externally visible behavior. Confirm null and absence behavior, duplicate-key behavior, ordering and mutability, exception contracts, state changes, authorization, transaction boundaries, and side-effect order.

Choose the smallest remedy that preserves the contract: local cleanup, standard library facility, stronger type, immutable value, ordinary helper, enum or record, JDK functional interface, domain-named functional interface, multi-method strategy, application service, architectural follow-up, or no change.

Functional interfaces are one possible result, not the goal. Use one only when a stable algorithm has one genuinely substitutable behavior. Do not hide consequential I/O or lifecycle effects in generic `Consumer` chains, and do not convert variation that is merely data into a `Function`.

## Report the audit

Lead with the highest-value evidence-backed candidates. For each, give the exact location, current pattern, actual variation or unique risk, recommended remedy, contract risks, smallest safe next step, and verification boundary.

Include a coverage statement listing source roots, file counts, mechanical signals, semantic samples, exclusions, and remaining uncertainty. Separate low-risk cleanup, contract-sensitive refactoring, specialist follow-ups, and improvements that require measurement.
