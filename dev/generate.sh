#!/bin/bash
# Convenience script to regenerate documentation
# Run from anywhere: ./dev/generate.sh

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "🔧 Django-Trim Documentation Generator"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ -f ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
    echo "✓ Using virtual environment: .venv"
elif [ -f "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
    echo "✓ Using virtual environment: venv"
else
    PYTHON="python3"
    echo "⚠ Using system Python (no venv detected)"
fi

echo ""
echo "Running: $PYTHON dev/gen_docs_standalone.py"
echo ""

$PYTHON dev/gen_docs_standalone.py

echo ""
echo "✅ Done!"
