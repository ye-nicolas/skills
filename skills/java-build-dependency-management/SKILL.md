---
name: java-build-dependency-management
description: Change or review Java Maven and Gradle builds, dependency versions, BOMs, plugins, toolchains, modules, generated sources, and reproducibility. Use for build failures caused by configuration, dependency upgrades, convergence conflicts, JDK migrations, or build-logic changes; do not replace the repository's established build system without an explicit migration request.
---

# Java Build and Dependency Management

Make the smallest build or dependency change that satisfies the requested
capability while preserving contributor workflow, CI parity, publication
contracts, and reproducibility.

## Establish the build contract

Inspect before editing:

- repository instructions and the documented contributor command;
- Maven or Gradle wrapper versions, root and module build files, settings,
  catalogs, BOMs, lockfiles, plugin management, repositories, and toolchains;
- CI JDK, profiles, flags, caches, generated sources, packaging, and publishing;
- direct and relevant transitive dependencies, exclusions, scopes or
  configurations, and dependency constraints; and
- current failure, requested capability, compatibility range, and supported
  runtime environments.

Use the wrapper and existing high-level task. Do not guess plugin goals or task
names, silently migrate Maven to Gradle or vice versa, or introduce a version
catalog, parent, convention plugin, or buildSrc abstraction for a one-line need.

## Dependency changes

1. State why the dependency or version must change: feature, compatibility,
   security, bug fix, convergence, or removal.
2. Find the effective version owner: direct declaration, parent, BOM, catalog,
   platform, constraint, or plugin management.
3. Inspect affected callers and runtime behavior, not only whether resolution
   succeeds. Check release notes or primary documentation when compatibility is
   uncertain and network access is available.
4. Prefer one authoritative version declaration. Avoid duplicate overrides that
   hide the effective graph.
5. Preserve scopes/configurations and exclude transitives only with evidence of
   a conflict, vulnerability, duplicate capability, or unwanted runtime surface.
6. Update lockfiles or verification metadata through the repository's normal
   workflow when they are intentionally owned artifacts.

For security updates, use `$springboot-security` when exploitability and
reachability require application-level review. A scanner finding alone does not
prove the vulnerable path is reachable, but a successful build alone does not
prove the upgrade is behaviorally compatible.

## Build logic and toolchains

- Keep JDK source/target/release and test/runtime toolchains aligned with the
  supported compatibility contract.
- Preserve multi-module dependency direction and published coordinates. Treat
  artifact names, classifiers, module metadata, and generated API sources as
  compatibility surfaces.
- Prefer built-in Maven/Gradle and established plugin capabilities before custom
  scripting. Keep custom build logic cohesive and testable when it has real
  branching or reuse.
- Separate developer convenience from CI/release requirements. A local cache hit
  or IDE build is not proof of a clean reproducible build.
- Do not add repositories casually. Check trust, availability, credential
  handling, content filters, and precedence.

## Diagnose resolution and build failures

Use dependency insight/tree output, effective configuration, and the earliest
meaningful build error to identify the owner of a conflict. Distinguish:

- unavailable artifact or repository authentication;
- version convergence or incompatible binary/API change;
- plugin/toolchain/JDK incompatibility;
- duplicate classes, service providers, or annotation processors;
- generated-source ordering or incremental-build defects; and
- environmental network, cache, filesystem, Docker, or sandbox failures.

Use `$java-debugging` when the resolved build succeeds but runtime or test
behavior is wrong.

## Verification

Run the configured formatter or build-file check, dependency resolution, the
smallest affected compile/test task, and the repository's required broader gate.
For dependency or toolchain changes, prefer a clean build when practical and
verify packaging or publication metadata when it changed. Inspect the final
dependency graph and diff for unrelated version churn.

Use `$java-verification` to gather the complete project evidence. Report exact
commands, effective versions, affected modules, compatibility assumptions, and
any verification blocked by unavailable repositories or services.
