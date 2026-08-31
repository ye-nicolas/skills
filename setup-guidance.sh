#!/usr/bin/env bash

set -eu

# Determine repository root absolute path
REPO_DIR="$(cd "$(dirname "$0")" && pwd -P)"
if [ "$REPO_DIR" = "." ] || [ -z "$REPO_DIR" ]; then
  REPO_DIR="$(pwd -P)"
fi

CODEX_DIR="$HOME/.codex"

echo "🚀 Setting up global agent guidance..."
echo "Repository: $REPO_DIR"
echo "This optional setup affects all Codex projects for the current user."

mkdir -p "$CODEX_DIR"
echo "📋 Processing AGENTS.md and SOP files -> $CODEX_DIR..."

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

echo "✅ Global guidance setup complete!"
