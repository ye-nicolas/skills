# Skill inventory

This document records the skill inventory observed on 2026-08-31. It separates
content maintained by this repository from skills supplied by Codex or found in
the local plugin cache. It also records the global Codex instruction files
maintained alongside the skills.

Cache presence proves that plugin files were downloaded. It does not prove that
the plugin or every cached skill is currently enabled.

## Management states

- **Version controlled**: the complete skill directory is maintained under
  `skills/` in this repository.
- **Bundled system**: the skill is supplied by Codex under
  `~/.codex/skills/.system` and is not copied into this repository.
- **Plugin cache**: the skill is supplied by a downloaded plugin under
  `~/.codex/plugins/cache` and is recorded here without vendoring its files.

Codex supports repository, user, administrator, and system skill locations, as
well as symlinked skill directories. See the
[official skill documentation](https://learn.chatgpt.com/docs/build-skills).

## Version-controlled skills

Repository remote:

```text
git@github.com:ye-nicolas/skills.git
```

These 32 skills are the source of truth for the symlinked user skill locations.
The local copies did not contain nested Git metadata. Exact upstream commits
therefore cannot be reconstructed, and most upstream repositories cannot be
established from the files alone. Links used only as examples or design
references are not treated as download provenance.

### Provenance and licensing status

A frontmatter license identifier is recorded below as a declaration only. It
does not replace the full license text or prove that every bundled file is
covered by that license. Archived local Codex session history proves that four
skills were downloaded on 2026-08-27 from moving branch heads; their exact
commit SHAs were not captured.

| Skill | Status | Recorded origin or upstream | License evidence | Public redistribution status |
| --- | --- | --- | --- | --- |
| `observability` | Downloaded, then adapted | [NotHarshhaa/devops-skills](https://github.com/NotHarshhaa/devops-skills/tree/master/observability), `master` | MIT; local version `1.1.0` names `devops-skills contributors` | Full upstream MIT notice and a modification record are required before push |
| `observability-designer` | Downloaded | [borghei/Claude-Skills](https://github.com/borghei/Claude-Skills/tree/main/engineering/observability-designer), `main` | MIT + Commons Clause, Copyright 2025-2026 Amin Borghei | Complete upstream notice is required; selling or paid repackaging is restricted |
| `otel-instrumentation` | Downloaded, then adapted | [dash0hq/agent-skills](https://github.com/dash0hq/agent-skills/tree/main/skills/otel-instrumentation), `main` | Apache-2.0, Copyright 2025 Dash0 Inc. | Full license, retained notices, and prominent modification notices are required before push |
| `github-repo-explore` | Downloaded | [microsoft/semantic-link-labs](https://github.com/microsoft/semantic-link-labs/tree/main/.claude/skills/github-repo-explore), `main` | MIT, Copyright Microsoft Corporation | Full upstream MIT notice is required before push |
| `effective-java-core` | Pure original `SKILL.md` | Originally cited [HugoMatilla/Effective-JAVA-Summary](https://github.com/HugoMatilla/Effective-JAVA-Summary) | Legacy un-licensed excerpts purged | Cleared: all third-party unlicensed references removed; SKILL.md is clean |
| `effective-java-concurrency` | Pure original rules & JDK docs | Oracle/OpenJDK JEPs & original SKILL rules | Uncredited Russian `thread-pools.md` purged | Cleared: thread-pools.md removed; references standard JDK 21+ docs |
| `conventional-commits-zh` | Unverified translation excerpt | Likely derived from [Conventional Commits](https://github.com/conventional-commits/conventionalcommits.org), but the exact translation source is not locally recorded | Upstream specification is MIT; local translation provenance is unverified | Blocked until source and license coverage are confirmed or the excerpt is rewritten |
| `jpa-patterns`, `springboot-patterns`, `springboot-security`, `springboot-tdd` | Unresolved marker | Frontmatter contains `origin: ECC`; `ECC` is not defined locally | Not recorded | Origin and redistribution terms remain unverified |
| Remaining skills | Locally maintained, authorship not recorded | No installation source or upstream metadata found | Not recorded | Confirm local authorship before treating them as publishable original work |

The inventory repository is publicly readable. Items marked **Blocked** must
not be committed until their redistribution conditions are resolved. This is
an inventory control, not legal advice.

### Java and JVM

- `effective-java-concurrency`
- `effective-java-core`
- `java-architecture-review`
- `java-build-dependency-management`
- `java-code-review`
- `java-debugging`
- `java-engineering-navigator`
- `java-implementation-planning`
- `java-junit`
- `java-performance-engineering`
- `java-refactoring-opportunity-audit`
- `java-verification`
- `jpa-patterns`
- `maintainable-java-code`

### Spring

- `spring-messaging-patterns`
- `springboot-patterns`
- `springboot-reactive-patterns`
- `springboot-security`
- `springboot-tdd`
- `springboot-testing`

### Observability

- `observability`
- `observability-designer`
- `observability-workflow`
- `otel-instrumentation`

### Engineering workflows

- `behavior-outcome-analysis`
- `commit-msg`
- `contract-first-refactoring`
- `conventional-commits-zh`
- `github-repo-explore`
- `markdown-docs`
- `requirements-interview`
- `scan-project-git`

## Version-controlled global guidance

The active global Codex guidance was observed at `~/.codex/AGENTS.md`. No
`~/.codex/AGENTS.override.md` was present, and `CODEX_HOME` was not set during
the inventory. The live files are symlinked to the following repository files:

- `config/AGENTS.md`
- `config/PROJECT_EXECUTION.execution.md`
- `config/PROJECT_EXECUTION.initialization.md`
- `config/PROJECT_EXECUTION.test-doubles.md`
- `config/PROJECT_EXECUTION.verification.md`

The four `PROJECT_EXECUTION.*.md` files are included because
`config/AGENTS.md` conditionally references them. Keeping the set together
makes the global guidance reproducible on another machine.

Codex reads global guidance from its home directory, using
`AGENTS.override.md` when present and otherwise `AGENTS.md`. See the
[official AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Bundled system skills

The following six skills were observed under `~/.codex/skills/.system`. Their
contents and lifecycle remain managed by Codex.

- `imagegen`
- `openai-docs`
- `plugin-creator`
- `review-agent`
- `skill-creator`
- `skill-installer`

## Downloaded plugin skill cache

The local cache contained 45 `SKILL.md` files across 11 plugin packages.
Versions and Git sources below come from each plugin's local
`.codex-plugin/plugin.json` metadata. A missing source means the manifest did not
declare a repository.

| Distribution | Plugin | Version | Git source | Skill count |
| --- | --- | --- | --- | ---: |
| OpenAI bundled | `browser` | `26.825.51511` | [openai/openai browser plugin](https://github.com/openai/openai/tree/master/lib/browser_use/plugin) | 1 |
| OpenAI bundled | `sites` | `0.1.46` | Not declared | 2 |
| OpenAI bundled | `visualize` | `1.0.23` | Not declared | 1 |
| OpenAI curated | `superpowers` | `5.1.3` (`bd2122cb` cache revision) | [obra/superpowers](https://github.com/obra/superpowers) | 14 |
| OpenAI curated remote | `openai-templates` | `0.1.1` | [openai/oai-maintained-plugins](https://github.com/openai/oai-maintained-plugins/tree/main/plugins/openai-templates) | 20 |
| OpenAI curated remote | `plugin-management` | `0.1.0` | [openai/openai plugin-management](https://github.com/openai/openai/tree/master/chatgpt/oai-maintained-plugins/plugins/plugin-management) | 1 |
| OpenAI primary runtime | `documents` | `26.826.12353` | [openai/openai](https://github.com/openai/openai) | 1 |
| OpenAI primary runtime | `pdf` | `26.826.12353` | [openai/openai](https://github.com/openai/openai) | 1 |
| OpenAI primary runtime | `presentations` | `26.826.12353` | [openai/openai](https://github.com/openai/openai) | 1 |
| OpenAI primary runtime | `spreadsheets` | `26.826.12353` | [openai/openai](https://github.com/openai/openai) | 2 |
| OpenAI primary runtime | `template-creator` | `26.826.12353` | [openai/openai](https://github.com/openai/openai) | 1 |

### Cached skill names

- `browser`: `control-in-app-browser`
- `sites`: `sites-building`, `sites-hosting`
- `visualize`: `visualize`
- `superpowers`: `brainstorming`, `dispatching-parallel-agents`,
  `executing-plans`, `finishing-a-development-branch`,
  `receiving-code-review`, `requesting-code-review`,
  `subagent-driven-development`, `systematic-debugging`,
  `test-driven-development`, `using-git-worktrees`, `using-superpowers`,
  `verification-before-completion`, `writing-plans`, `writing-skills`
- `openai-templates`: `artifact-template-analytics-dashboard`,
  `artifact-template-business-review`, `artifact-template-design-report`,
  `artifact-template-experiment-analysis`, `artifact-template-financial-budget`,
  `artifact-template-investment-committee-memo`,
  `artifact-template-legal-memorandum`, `artifact-template-market-trends-report`,
  `artifact-template-minimal-letterhead`, `artifact-template-operating-calendar`,
  `artifact-template-operating-review`, `artifact-template-project-kickoff`,
  `artifact-template-project-tracker`, `artifact-template-sales-pipeline`,
  `artifact-template-simple-dark-mode`, `artifact-template-simple-light-mode`,
  `artifact-template-strategy-memorandum`, `artifact-template-system-design`,
  `artifact-template-team-alignment`, `artifact-template-three-statement-forecast`
- `plugin-management`: `plugin-management`
- `documents`: `documents`
- `pdf`: `pdf`
- `presentations`: `presentations`
- `spreadsheets`: `excel-live-control`, `spreadsheets`
- `template-creator`: `template-creator`

Downloaded plugins without a `SKILL.md`, such as `codex-app-tools` and
`github`, are outside this skill inventory.

## Maintenance

Update this snapshot when any of the following changes:

- a skill is added to or removed from `skills/`;
- a global guidance file is added, removed, or renamed under `config/`;
- a bundled system skill appears or disappears;
- a plugin version or cache revision changes;
- a plugin adds or removes a `SKILL.md` file;
- previously unknown source metadata becomes available.

When downloading a skill in the future, record its source URL, installation
command, acquisition date, tag or commit, author, license identifier, and a
copy of any upstream `LICENSE`, `NOTICE`, or `COPYING` file at the same time.
