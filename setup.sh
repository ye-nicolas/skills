#!/usr/bin/env bash

set -e

MODE="${1:-all}"

# Determine repository root absolute path
REPO_DIR="$(cd "$(dirname "$0")" && pwd -P)"
if [ "$REPO_DIR" = "." ] || [ -z "$REPO_DIR" ]; then
  REPO_DIR="$(pwd -P)"
fi

AGENTS_SKILLS_DIR="$HOME/.agents/skills"
CODEX_DIR="$HOME/.codex"

echo "🚀 Running setup (Mode: $MODE)..."
echo "Repository: $REPO_DIR"

# 1. Symlink skills/* to ~/.agents/skills/
if [ "$MODE" = "all" ] || [ "$MODE" = "skills" ]; then
  mkdir -p "$AGENTS_SKILLS_DIR"
  echo "📦 Processing skills -> $AGENTS_SKILLS_DIR..."

  for skill_path in "$REPO_DIR/skills"/*; do
    if [ -d "$skill_path" ]; then
      skill_name="$(basename "$skill_path")"
      target_link="$AGENTS_SKILLS_DIR/$skill_name"
      abs_skill_path="$(cd "$skill_path" && pwd -P)"
      
      # Check if target link already exists and is pointing to the correct source
      if [ -L "$target_link" ]; then
        current_target="$(readlink "$target_link")"
        if [ "$current_target" = "$abs_skill_path" ] || [ "$current_target" = "$skill_path" ]; then
          echo "  - [Already Linked] $skill_name"
          continue
        fi
      elif [ -e "$target_link" ]; then
        echo "  - ⚠️  [Backup] Target $target_link is a real directory/file. Backing up to ${target_link}.bak"
        mv "$target_link" "${target_link}.bak"
      fi

      ln -sfn "$abs_skill_path" "$target_link"
      echo "  - [Linked] $skill_name"
    fi
  done

  # Cleanup dangling symlinks in ~/.agents/skills
  for link in "$AGENTS_SKILLS_DIR"/*; do
    if [ -L "$link" ]; then
      target="$(readlink "$link")"
      case "$target" in
        "$REPO_DIR/skills/"*)
          if [ ! -e "$target" ]; then
            echo "  - 🧹 [Cleanup Stale Link] Removing broken link: $(basename "$link")"
            rm -f "$link"
          fi
          ;;
      esac
    fi
  done
fi

# 2. Symlink config/AGENTS.md and SOP files to ~/.codex/
if [ "$MODE" = "all" ] || [ "$MODE" = "agents" ] || [ "$MODE" = "guidance" ]; then
  mkdir -p "$CODEX_DIR"
  echo "📋 Processing global guidance (AGENTS.md & SOPs) -> $CODEX_DIR..."

  for config_file in "$REPO_DIR/config"/*.md; do
    if [ -f "$config_file" ]; then
      file_name="$(basename "$config_file")"
      target_link="$CODEX_DIR/$file_name"
      abs_config_file="$(cd "$(dirname "$config_file")" && pwd -P)/$file_name"
      
      if [ -L "$target_link" ]; then
        current_target="$(readlink "$target_link")"
        if [ "$current_target" = "$abs_config_file" ] || [ "$current_target" = "$config_file" ]; then
          echo "  - [Already Linked] $file_name"
          continue
        fi
      elif [ -e "$target_link" ]; then
        echo "  - ⚠️  [Backup] Target $target_link is a real file. Backing up to ${target_link}.bak"
        mv "$target_link" "${target_link}.bak"
      fi

      ln -sfn "$abs_config_file" "$target_link"
      echo "  - [Linked] $file_name"
    fi
  done
fi

echo "✅ Setup complete for mode '$MODE'!"
