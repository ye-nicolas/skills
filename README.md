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
├── skills/                  # Version-controlled Agent Skills (~/.agents/skills)
│   ├── java-code-review/
│   │   └── SKILL.md
│   ├── observability/
│   └── ... (32 skills total)
├── Makefile                 # Commands for quick linking & cleanup
└── setup.sh                 # Environment setup script
```

## 🚀 Quick Start

Run `make` from the repository root to link all skills to `~/.agents/skills` and global guidance files to `~/.codex`:

```bash
make
```

### Available `make` Targets

| Target | Command | Description |
| :--- | :--- | :--- |
| **`setup`** *(default)* | `make` / `make setup` | Link skills to `~/.agents/skills` and guidance to `~/.codex` |
| **`skills`** | `make skills` | Link ONLY skills to `~/.agents/skills` |
| **`agents`** | `make agents` | Link ONLY AGENTS.md and SOP files to `~/.codex` |
| **`status`** | `make status` | Inspect current symlink status in environment |
| **`clean`** | `make clean` | Remove all symlinks created from this repository |
| **`help`** | `make help` | Show available Makefile targets |

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
