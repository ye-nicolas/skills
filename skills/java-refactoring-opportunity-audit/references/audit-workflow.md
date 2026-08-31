# Repository-wide Java audit workflow

Use this workflow to discover candidates across a repository rather than only reviewing code already known to be interesting. Similar code is one discovery lane; unique but high-impact code must also be inspected.

## Role boundary

This is a discovery and triage workflow. Screen broadly, validate the highest-value candidates, and route specialist concerns instead of duplicating full architecture, security, concurrency, persistence, messaging, reactive, or performance reviews. Do not implement findings as part of the audit unless the user explicitly expands the task.

## 1. Inventory before sampling

- Locate Java source roots, modules, generated-code directories, build files, tests, and repository instructions.
- Record the configured JDK and framework style.
- Count Java files and rank large classes.
- Identify repeated class basenames and high-fan-in utilities before choosing representative files.
- Exclude generated sources and build output from findings unless the user asks about them.

Run the bundled scanner from the repository or module root:

```bash
python3 /path/to/skill/scripts/scan_java_refactoring_candidates.py .
```

The scanner deliberately favors recall over precision. Inspect every reported candidate before describing it as a problem.

## 2. Search both functional and imperative forms

Do not equate functional opportunities with code that already contains lambdas.

Inspect these signal groups:

- Existing functional syntax: lambdas, method references, streams, collectors, anonymous implementations of functional types.
- Repeated imperative transformations: `for` plus `Map.put`, `List.add`, filtering conditions, accumulator updates, and repeated sort comparators.
- Behavior selection: `if` or `switch` branches that differ only by a method call, query builder, mapper, validator, or response transformation.
- Repeated construction: DTO, message, query, or export payload builders whose stable fields dominate the variation.
- Parallel hierarchies: similarly named controllers or services for house, master-agent, agent, player, vendor, role, or report type.
- Utility concentration: static helper classes with many callers or many same-shaped methods.

Use `rg` for targeted follow-up. Normalize only known naming variations when comparing paired files; keep the raw diff available so normalization cannot hide real semantic differences.

## 3. Inspect non-duplication improvement lanes

Mechanically duplicated code is not the only source of maintenance risk. Sample important and high-fan-in code for:

- package dependencies that point from data or domain code toward controllers;
- raw types, unchecked casts, stringly typed composite keys, and generic maps used as long-lived contracts;
- mutable utility classes, unnecessary generated methods or constructors, and overly broad visibility;
- `Optional.orElse(null)`, nullable collection returns, and ambiguous empty-versus-absent behavior;
- repeated or broad catch blocks, swallowed causes, and response construction mixed with business work;
- stream stages used only for side effects, redundant collects, and pipelines that obscure failure or mutation;
- asynchronous or transactional effects whose ownership, executor, cancellation, or ordering is unclear;
- mutable logging context or request-log objects whose identifiers are generated, overwritten, or assigned after a log event;
- dead branches, old implementations still wired beside replacements, commented-out security checks, stale TODOs, and misleading names;
- large classes and methods with several independent reasons to change, even when there is no clone.

Treat each signal as a lead. A locally unusual construct may be correct because of serialization, persistence, framework, or compatibility constraints.

When a candidate involves request-log objects, correlation identifiers, MDC, or logging context across asynchronous work, read [logging-correlation-context.md](logging-correlation-context.md) before deciding whether the lifecycle or carrier is correct.

## 4. Recover the contract

For each strong candidate, answer:

1. What inputs and outputs are valid?
2. What do `null`, empty values, missing values, and duplicate keys mean?
3. Are returned collections mutable, ordered, or shared?
4. Which checked and unchecked failures can callers observe?
5. Which database, cache, message, filesystem, or remote-call effects occur, and in what order?
6. Are authorization, transaction, retry, concurrency, or logging boundaries different between copies?
7. Is the apparent variation behavior, or is it only a value such as an enum, topic, response code, or hierarchy?

Trace important callers and tests. Similar bodies with divergent permission checks or exception handling are a contract question first, not a mechanical consolidation.

## 5. Classify the smallest suitable abstraction

| Situation | Prefer | Avoid |
| --- | --- | --- |
| One input is transformed to one output | `Function<T, R>` or method reference | A domain interface with no added meaning |
| Pure yes/no rule | `Predicate<T>` | Predicate when callers need distinct rejection reasons |
| Lazy value construction | `Supplier<T>` | Supplier that hides I/O or lifecycle ownership |
| Value-preserving transform | `UnaryOperator<T>` | General `Function<T, T>` when operator intent is clearer |
| Duplicate-value resolution or combination | `BinaryOperator<T>` | A collector that silently changes duplicate semantics |
| Meaningful business operation or checked failure | Domain-named `@FunctionalInterface` | Wrapping checked failures in generic runtime exceptions |
| Several correlated variations | Named strategy/policy object | A constructor containing a bag of unrelated functions |
| Variation is topic, status, hierarchy, or response code | Enum, record, or parameter | `Function` used only to carry data |
| Shared side-effect sequence | Application service/template with explicit steps | Generic `Consumer` chains that hide effect order |

An abstraction should remove more decisions than it introduces. Retain domain-named wrapper methods when they communicate a useful contract; remove them when they only delegate without meaning.

## 6. Report coverage and priorities

Report:

- source roots and file counts screened;
- signals used, including both functional and imperative patterns;
- high-confidence candidates with exact locations and callers;
- candidates that need business clarification;
- patterns checked but intentionally not abstracted;
- excluded or uninspected areas.

Prioritize by maintenance cost, caller count, business criticality, semantic stability, testability, and migration risk. A small high-fan-in lookup abstraction can be a better first change than a large duplicated controller whose authorization contract is unclear; a unique but unsafe boundary may outrank both.
