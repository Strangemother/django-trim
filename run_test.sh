#!/usr/bin/env bash
# Legacy test script - use ./quicktest instead for better options
# This script is kept for backwards compatibility

echo "Note: Consider using ./quicktest for more options"
echo "Running tests with pytest..."
echo ""

export PYTHONPATH="$PWD/src:$PYTHONPATH"
export DJANGO_SETTINGS_MODULE="tests.settings"

python3 -m pytest tests/ -v --cov=trim --cov-report=xml --cov-report=html --cov-report=term-missing "$@"