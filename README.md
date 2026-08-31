# Agent Skills & Global Guidance Repository

Personal version-controlled collection of 32 reusable Agent Skills for software engineering workflows, along with global AI agent working agreements (`AGENTS.md`).

## 📁 Repository Structure

```text
skills/
├── config/                  # Global AI agent guidance & execution SOPs (~/.codex)
│   ├── AGENTS.md            # Global working agreements
│   └── PROJECT_EXECUTION.*  # Conditional execution workflows
├── docs/                    # Documentation & Inventory
│   └── skill-inventory.md   # Skill inventory snapshot & license provenance
├── skills/                  # Version-controlled Agent Skills
│   ├── java-code-review/
│   │   └── SKILL.md
│   ├── observability/
│   └── ... (32 skills total)
└── setup-guidance.sh        # Optional global guidance setup script
```

## Prerequisites

- Node.js and npm, which provide `npx`
- Codex, when installing with `--agent codex`

Verify the required commands before installing:

```bash
node --version
npx --version
```

The `skills` CLI is downloaded by `npx` when needed; it is not bundled with Codex and does not require a separate global npm installation.

## 🚀 Quick Start

### Install the skills

Preview the skills available in this repository without installing them:

```bash
npx skills add ye-nicolas/skills --list
```

Install every skill globally for Codex:

```bash
npx skills add ye-nicolas/skills --global --agent codex --skill '*'
```

Install only selected skills by name:

```bash
npx skills add ye-nicolas/skills \
  --global \
  --agent codex \
  --skill java-code-review \
  --skill springboot-testing
```

The `--global` option makes the installed skills available across projects. Without it, the CLI installs them for the current project only.

This standard installation only manages the Agent Skills under `skills/`. It does not modify global Codex guidance in `~/.codex`.

When developing or testing changes from a local checkout, use the repository path instead of the GitHub source:

```bash
npx skills add . --global --agent codex --skill '*'
```

### Verify and manage the installation

List the skills installed globally for Codex:

```bash
npx skills list --global --agent codex
```

Update globally installed skills:

```bash
npx skills update --global
```

Remove installed skills interactively:

```bash
npx skills remove --global --agent codex
```

Installed skills are available to Codex on the next turn.

For a private repository, installers must already have GitHub access through their Git credentials. They can use the SSH source form:

```bash
npx skills add git@github.com:ye-nicolas/skills.git \
  --global \
  --agent codex \
  --skill '*'
```

### Optional: install global guidance

The files under `config/` define global working agreements for Codex. Installing them affects every Codex project for the current user, so review them before opting in.

Clone the repository, then run the dedicated guidance setup script:

```bash
git clone https://github.com/ye-nicolas/skills.git
cd skills
./setup-guidance.sh
```

The script links `config/AGENTS.md` and `config/PROJECT_EXECUTION.*.md` into `~/.codex`. If a destination is an existing regular file, the script first moves it to a `.bak` backup.

---

## 🧰 Skill Inventory (32 Skills)

Skills are organized into four core categories:

### ☕ Java & JVM (14 Skills)
- **`effective-java-concurrency`** — Java concurrency & thread-safety patterns (Effective Java)
- **`effective-java-core`** — Core Java object design & immutability best practices
- **`java-architecture-review`** — Architectural & structural pattern review for Java projects
- **`java-build-dependency-management`** — Build configurations & dependency optimization (Maven/Gradle/uv)
- **`java-code-review`** — Standard Java code review checklists & quality rules
- **`java-debugging`** — Diagnostic strategies & root cause analysis for JVM exceptions
- **`java-engineering-navigator`** — Navigation & mapping of complex Java codebases
- **`java-implementation-planning`** — Step-by-step refactoring & feature implementation plans
- **`java-junit`** — JUnit 5 unit testing patterns & assertion best practices
- **`java-performance-engineering`** — JVM tuning, memory analysis & performance optimization
- **`java-refactoring-opportunity-audit`** — Identification of code smells & technical debt
- **`java-verification`** — Automated build & test verification workflows
- **`jpa-patterns`** — Spring Data JPA & Hibernate entity mapping/query optimization
- **`maintainable-java-code`** — Clean code principles & maintainability guidelines

### 🍃 Spring Framework (6 Skills)
- **`spring-messaging-patterns`** — Event-driven architecture, messaging & listener patterns
- **`springboot-patterns`** — Spring Boot application conventions & auto-configurations
- **`springboot-reactive-patterns`** — Spring WebFlux & reactive stream processing
- **`springboot-security`** — Spring Security authentication & authorization patterns
- **`springboot-tdd`** — Test-Driven Development (TDD) workflow for Spring Boot
- **`springboot-testing`** — Integration testing (@SpringBootTest, MockBean, Testcontainers)

### 📊 Observability (4 Skills)
- **`observability`** — Observability strategy, metrics, and tracing setup
- **`observability-designer`** — Metrics & log format design guidelines
- **`observability-workflow`** — Step-by-step telemetry implementation workflow
- **`otel-instrumentation`** — OpenTelemetry SDK & auto-instrumentation patterns

### 🛠️ Engineering Workflows (8 Skills)
- **`behavior-outcome-analysis`** — System behavior & outcome verification analysis
- **`commit-msg`** — Git commit message generation & formatting guidelines
- **`contract-first-refactoring`** — API & contract-first refactoring patterns
- **`conventional-commits-zh`** — Conventional Commits spec & Chinese reference
- **`github-repo-explore`** — Exploration & analysis of external GitHub repositories
- **`markdown-docs`** — Documentation structure & technical documentation rules
- **`requirements-interview`** — Interactive requirements elicitation & clarification
- **`scan-project-git`** — Git commit history & repository health audit

*For detailed provenance, licenses, and local plugin cache info, see [docs/skill-inventory.md](docs/skill-inventory.md).*

---

## 📋 Global AI Agent Guidance (`config/`)

The `config/` directory contains global working agreements and conditional execution SOPs for AI coding agents:

- **`config/AGENTS.md`**: Core working agreements, Java standards, and output requirements.
- **`config/PROJECT_EXECUTION.*.md`**: Conditional execution workflows covering task decomposition, project initialization, test-doubles, and verification protocols.

> **Note**: Storing guidance under `config/` allows it to be globally symlinked into `~/.codex/` without creating a repository-scoped `AGENTS.md` at the root of this repository.

---

## 📐 Conventions

- **Focused Scope**: Each skill must address a single, well-defined workflow.
- **Naming**: Use lowercase letters, numbers, and hyphens for directory names (e.g., `effective-java-core`).
- **Structure**: Maintain primary instructions inside `SKILL.md`; add `scripts/`, `references/`, or `assets/` only when necessary.
- **Security**: Never commit secrets, credentials, API keys, or machine-specific paths.
