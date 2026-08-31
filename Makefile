.PHONY: all setup setup-skills setup-agents skills agents guidance status status-skills status-agents clean clean-skills clean-agents help

# Default target
all: setup

## setup: Link both skills (~/.agents/skills) and agents guidance (~/.codex)
setup:
	@./setup.sh all

## skills: Link ONLY skills to ~/.agents/skills
skills: setup-skills

setup-skills:
	@./setup.sh skills

## agents: Link ONLY AGENTS.md and SOP files to ~/.codex
agents: setup-agents

guidance: setup-agents

setup-agents:
	@./setup.sh agents

## status: Check symlink status for both skills and agents guidance
status: status-skills status-agents

status-skills:
	@echo "🔍 Checking symlink status in ~/.agents/skills..."
	@ls -la ~/.agents/skills 2>/dev/null || echo "Directory ~/.agents/skills does not exist."

status-agents:
	@echo "🔍 Checking symlink status in ~/.codex..."
	@ls -la ~/.codex/*.md 2>/dev/null || echo "No guidance markdown files linked in ~/.codex."

## clean: Remove all symlinks created from this repository
clean: clean-skills clean-agents
	@echo "✅ Complete cleanup finished."

clean-skills:
	@echo "🧹 Unlinking skills from ~/.agents/skills..."
	@repo_dir="$$(pwd -P)"; \
	for link in $$HOME/.agents/skills/*; do \
		if [ -L "$$link" ]; then \
			target="$$(readlink "$$link")"; \
			case "$$target" in \
				"$$repo_dir/skills/"*) \
					echo "  - Unlinking skill: $$(basename "$$link")"; \
					rm -f "$$link"; \
					;; \
			esac; \
		fi; \
	done

clean-agents:
	@echo "🧹 Unlinking agents guidance from ~/.codex..."
	@repo_dir="$$(pwd -P)"; \
	for link in $$HOME/.codex/*.md; do \
		if [ -L "$$link" ]; then \
			target="$$(readlink "$$link")"; \
			case "$$target" in \
				"$$repo_dir/config/"*) \
					echo "  - Unlinking guidance: $$(basename "$$link")"; \
					rm -f "$$link"; \
					;; \
			esac; \
		fi; \
	done

## help: Show this help message
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup        (Default) Link both skills and AGENTS.md guidance"
	@echo "  skills       Link ONLY skills to ~/.agents/skills"
	@echo "  agents       Link ONLY AGENTS.md and SOP files to ~/.codex"
	@echo "  status       Check status of both skills and agents guidance"
	@echo "  clean        Remove all symlinks created by this repo"
	@echo "  clean-skills Remove only skill symlinks"
	@echo "  clean-agents Remove only AGENTS.md guidance symlinks"
	@echo "  help         Show this help message"
