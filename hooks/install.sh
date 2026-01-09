#!/bin/bash
# Install git hooks for django-trim project

HOOKS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GIT_HOOKS_DIR="$(git rev-parse --git-dir)/hooks"

echo "Installing git hooks..."
echo "Source: $HOOKS_DIR"
echo "Target: $GIT_HOOKS_DIR"
echo ""

# Install pre-push hook
if [ -f "$GIT_HOOKS_DIR/pre-push" ]; then
    echo "⚠️  pre-push hook already exists"
    read -p "Overwrite? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "Skipping pre-push hook"
    else
        cp "$HOOKS_DIR/pre-push" "$GIT_HOOKS_DIR/pre-push"
        chmod +x "$GIT_HOOKS_DIR/pre-push"
        echo "✅ Installed pre-push hook"
    fi
else
    cp "$HOOKS_DIR/pre-push" "$GIT_HOOKS_DIR/pre-push"
    chmod +x "$GIT_HOOKS_DIR/pre-push"
    echo "✅ Installed pre-push hook"
fi

echo ""
echo "Done! Git hooks are now active."
echo "Run 'git push' to test the pre-push hook."
