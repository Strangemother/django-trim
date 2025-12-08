#!/usr/bin/env bash
# Setup script for django-trim testing infrastructure
# Run this first to install all test dependencies

set -e

echo "=========================================="
echo "  django-trim Testing Setup"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Found: $PYTHON_VERSION"
echo ""

# Install test dependencies
echo "Installing test dependencies..."
echo ""

# Option 1: Install from pyproject.toml (recommended)
if pip install -e ".[test]" 2>/dev/null; then
    echo "✓ Installed via pip install -e '.[test]'"
else
    # Option 2: Install from requirements file
    echo "Trying alternative installation method..."
    pip install -r requirements-test.txt
    pip install -e .
fi

echo ""
echo "✓ Test dependencies installed successfully!"
echo ""

# Install Django if not present
if ! python3 -c "import django" 2>/dev/null; then
    echo "Installing Django..."
    pip install "Django>=4.2,<5.0"
    echo "✓ Django installed"
else
    DJANGO_VERSION=$(python3 -c "import django; print(django.get_version())")
    echo "✓ Django $DJANGO_VERSION already installed"
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Quick Start Commands:"
echo ""
echo "  ./quicktest          # Run all tests"
echo "  ./quicktest -c       # Run with coverage"
echo "  ./quicktest --help   # Show all options"
echo ""
echo "For more information, see:"
echo "  - docs/TESTING.md"
echo "  - tests/README.md"
echo "  - TESTING_SETUP_COMPLETE.md"
echo ""
