#!/usr/bin/env bash
# Bootstrap Claude Code skills + config on a new machine
# Usage: git clone https://github.com/dsharm9148/claude-config /tmp/cc && bash /tmp/cc/setup.sh && rm -rf /tmp/cc

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
SKILLS_DIR="$HOME/claude-skills"

echo "Setting up Claude Code config..."

# --- Skills ---
mkdir -p "$SKILLS_DIR"

# Point ~/.claude/skills → ~/claude-skills if not already set
if [ ! -e "$CLAUDE_DIR/skills" ]; then
  ln -s "$SKILLS_DIR" "$CLAUDE_DIR/skills"
  echo "  ✓ Linked ~/.claude/skills → ~/claude-skills"
elif [ ! -L "$CLAUDE_DIR/skills" ]; then
  echo "  ! ~/.claude/skills exists and is not a symlink — skipping link"
fi

# Copy skill directories (skip if already present)
for skill_dir in "$REPO_DIR"/*/; do
  skill_name=$(basename "$skill_dir")
  [[ "$skill_name" == "_config" ]] && continue
  if [ ! -d "$SKILLS_DIR/$skill_name" ]; then
    cp -r "$skill_dir" "$SKILLS_DIR/$skill_name"
    echo "  ✓ Installed skill: $skill_name"
  else
    echo "  ~ Skipped (exists): $skill_name"
  fi
done

# career-ops: symlink if project is present
if [ -d "$HOME/career-ops/.claude/skills/career-ops" ] && [ ! -e "$SKILLS_DIR/career-ops" ]; then
  ln -s "$HOME/career-ops/.claude/skills/career-ops" "$SKILLS_DIR/career-ops"
  echo "  ✓ Linked career-ops skill"
fi

# --- Config files ---
mkdir -p "$CLAUDE_DIR/commands"

# CLAUDE.md
if [ ! -f "$CLAUDE_DIR/CLAUDE.md" ]; then
  cp "$REPO_DIR/_config/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
  echo "  ✓ Installed CLAUDE.md"
fi

# settings.json
if [ ! -f "$CLAUDE_DIR/settings.json" ]; then
  cp "$REPO_DIR/_config/settings.json" "$CLAUDE_DIR/settings.json"
  echo "  ✓ Installed settings.json"
fi

# commands
for cmd in "$REPO_DIR/_config/commands"/*.md; do
  fname=$(basename "$cmd")
  if [ ! -f "$CLAUDE_DIR/commands/$fname" ]; then
    cp "$cmd" "$CLAUDE_DIR/commands/$fname"
    echo "  ✓ Installed command: $fname"
  fi
done

echo ""
echo "Done. Skills: $(ls "$SKILLS_DIR" | grep -v '^_' | tr '\n' ' ')"
