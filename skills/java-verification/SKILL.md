---
name: java-verification
description: Verify Java and Spring changes or releases using the repository's configured formatter, build, static analysis, tests, coverage, security checks, and diff review. Use for completion evidence and release checks across plain Java, libraries, multi-module builds, and Spring applications; do not use as a generic implementation workflow.
---

# Java Project Verification

Gather completion evidence from the repository's actual contributor and CI
contract. Do not add plugins, invoke unconfigured goals, change production code,
or treat a text search match as a defect merely to complete this workflow.
Evidence must describe the current working tree or named revision. A previous
run, cached report, or remote CI result for another revision is context, not
proof that the current change passes.

## Discover the verification contract

Inspect, in order:

1. The requested behavior, approved plan or specification, acceptance criteria,
   and directly affected public contracts.
2. Repository and directory-specific instructions.
3. Makefile or task runner used by contributors and CI.
4. Maven or Gradle wrapper, modules, configured lifecycle, plugins, profiles,
   test source sets, and JDK toolchain.
5. CI workflows for required services, flags, coverage, packaging, publishing,
   and security gates.

Prefer the highest-level existing command that reproduces the intended gate.
Use focused lower-level commands for fast feedback only when their scope is
clear. Use `$java-build-dependency-management` when the task is to change the
build rather than verify it.

## Verification loop

1. **Requirement evidence:** map each acceptance criterion or planned behavior
   to a focused test, integration check, manual observation, or explicit gap.
   Passing unrelated tests does not prove the requested outcome.
2. **Format:** run the configured formatter or format check. Avoid unrelated
   rewrites; use check mode for review-only work.
3. **Compile/build:** compile every changed production path with the configured
   JDK and wrapper, including affected modules and generated sources.
4. **Focused tests:** run tests that directly exercise the changed behavior,
   including existing tests when only production code changed.
5. **Broader tests:** expand to the affected module or full suite for
   cross-cutting, high-risk, dependency, release, or explicitly requested work.
6. **Static analysis:** run only configured checkstyle, PMD, SpotBugs, Error
   Prone, nullness, architecture, API compatibility, or equivalent checks.
7. **Coverage:** apply repository thresholds when present. Report gaps as
   evidence; do not impose a universal percentage.
8. **Security:** run the configured dependency, secret, SAST, or container scan
   when relevant or release-required. Confirm findings before reporting them.
9. **Packaging/integration:** when relevant, verify the produced JAR, module
   metadata, startup/wiring, database or broker integration, and supported JDK.
10. **Diff review:** inspect status, diff/stat, generated files, configuration,
   dependency changes, temporary artifacts, and unintended scope.

For Spring code, include the smallest test that proves binding, wiring,
transactions, security, persistence, messaging, or reactive behavior when one
of those framework contracts changed. A successful application-context startup
does not replace a focused behavioral test.

## Failure handling

- Record unrelated existing failures separately instead of fixing them without
  authorization.
- Retry only when a failure is plausibly environmental and the retry follows
  the normal permission and dependency path.
- Do not change code to hide a JDK attach, Docker, network, sandbox, or cache
  problem.
- A successful compile does not replace a failed behavioral test. State the
  remaining verification gap.
- Distinguish `NOT CONFIGURED`, `NOT RUN`, and `FAIL`; they are not equivalent.

## Report

Summarize:

```text
Requirements:  PASS | FAIL | NOT DEFINED | NOT RUN — criteria and evidence
Format/static: PASS | FAIL | NOT CONFIGURED | NOT RUN
Build/package: PASS | FAIL | NOT RUN
Focused tests: PASS | FAIL | NOT RUN — scope
Broader tests: PASS | FAIL | NOT RUN — scope
Coverage:      PASS | FAIL | NOT CONFIGURED | NOT RUN — configured threshold
Security:      PASS | FAIL | NOT CONFIGURED | NOT RUN — confirmed findings
Integration:   PASS | FAIL | NOT APPLICABLE | NOT RUN — boundary
Diff review:   PASS | FAIL — scope notes
Overall:       VERIFIED | NOT VERIFIED
```

List exact commands, meaningful failures, and skipped evidence. Use `VERIFIED`
only when the requested behavior, current revision, and repository-required gate
have all passed.
