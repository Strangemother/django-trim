# Testing Setup Guide

Complete testing infrastructure for django-trim with multi-version Django support.

## Quick Start

```bash
# Install test dependencies
pip install -e ".[test]"

# Run all tests
./quicktest

# Run with coverage
./quicktest -c

# Run specific test
./quicktest -f test_mixin_order
```

## Installation

### Install Development Dependencies

```bash
# Install django-trim with test dependencies
pip install -e ".[test]"

# Or install manually
pip install pytest pytest-django pytest-cov pytest-xdist coverage[toml]
```

### Install Tox (for multi-version testing)

```bash
pip install tox
```

## Running Tests

### Using quicktest Script (Recommended)

The `quicktest` script provides an easy interface for running tests:

```bash
# Basic test run
./quicktest

# With coverage report
./quicktest -c

# Run specific test file or function
./quicktest -f test_trim_tests
./quicktest -f test_mixin_order

# Run tests in parallel (faster)
./quicktest -p

# Run with keyword filter
./quicktest -k "mixin and not slow"

# Exit on first failure
./quicktest -x

# Show print statements
./quicktest -s

# Run last failed tests
./quicktest --lf

# Combine options
./quicktest -c -p -x
```

### Multi-Version Django Testing

```bash
# Test all Django versions with tox
./quicktest -m

# Or use tox directly
tox

# Test specific Django version
./quicktest -v 4.2
./quicktest -v 5.0

# Test specific environment with tox
tox -e py311-django42
tox -e py312-django50
```

### Using pytest Directly

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=trim --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_trim_tests.py

# Run specific test function
pytest tests/test_trim_tests.py::TestMixinOrderValidation::test_correct_order_passes

# Run with keyword
pytest -k "mixin"

# Run in parallel
pytest -n auto

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Show print statements
pytest -s
```

## Test Structure

```
django-trim/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration & fixtures
│   ├── settings.py              # Django settings for testing
│   ├── urls.py                  # URL configuration for testing
│   ├── test_trim_tests.py       # Tests for trim.tests module
│   ├── test_functional.py       # Functional tests
│   ├── test_live.py             # Live model tests
│   ├── test_rand.py             # Random utilities tests
│   ├── test_urls.py             # URL utilities tests
│   └── test_updated_params.py   # Parameter update tests
├── quicktest                     # Quick test runner script
├── tox.ini                       # Tox configuration for multi-version tests
└── pyproject.toml                # pytest & coverage configuration
```

## Coverage Reports

### Generate Coverage Report

```bash
# HTML report (opens in browser)
./quicktest -c
open htmlcov/index.html

# Terminal report
pytest --cov=trim --cov-report=term-missing

# XML report (for CI)
pytest --cov=trim --cov-report=xml
```

### Coverage Configuration

Coverage settings are in `pyproject.toml`:

- **Source**: `src/trim`
- **Omit**: Tests, migrations, cache files
- **Branch coverage**: Enabled
- **Reports**: HTML, XML, terminal

## Supported Django Versions

django-trim supports current Django versions (as of Dec 2025):

| Python | Django 4.2 LTS | Django 5.0 | Django 5.1 | Django 5.2 | Django 6.0 |
|--------|---------------|-----------|-----------|-----------|-----------|
| 3.8    | ✓             | ✗         | ✗         | ✗         | ✗         |
| 3.9    | ✓             | ✗         | ✗         | ✗         | ✗         |
| 3.10   | ✓             | ✓         | ✓         | ✓         | ✓         |
| 3.11   | ✓             | ✓         | ✓         | ✓         | ✓         |
| 3.12   | ✓             | ✓         | ✓         | ✓         | ✓         |

**Key Versions:**
- **4.2** - LTS (Long Term Support until April 2026) - Most stable
- **5.2** - Current stable release
- **6.0** - Latest release

### Test Specific Version

```bash
# Create isolated environment and test
./quicktest -v 4.2   # LTS version
./quicktest -v 5.2   # Current stable
./quicktest -v 6.0   # Latest

# Or use tox directly
tox -e py311-dj42    # Django 4.2 LTS
tox -e py311-dj52    # Django 5.2
tox -e py311-dj60    # Django 6.0
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
        django-version: ['4.2', '5.0', '5.1']
        exclude:
          - python-version: '3.8'
            django-version: '5.0'
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -e ".[test]"
        pip install "Django~=${{ matrix.django-version }}.0"
    
    - name: Run tests
      run: |
        pytest --cov=trim --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Writing Tests

### Using trim.tests Utilities

```python
from django.test import TestCase
from trim import tests as trim_tests
from myapp import views


class ViewSecurityTests(TestCase):
    """Test view security configuration"""
    
    def test_all_views_mixin_order(self):
        """Ensure all views have correct mixin order"""
        trim_tests.assert_views_mixin_order(views)
    
    def test_specific_view(self):
        """Test specific view configuration"""
        trim_tests.assert_mixin_order(views.SecureEditView)
        trim_tests.assert_view_has_permission(
            views.SecureEditView,
            'myapp.change_model'
        )
```

### Using Fixtures

```python
def test_with_user(user):
    """Test with a regular user"""
    assert user.username == "testuser"


def test_with_staff(staff_user):
    """Test with a staff user"""
    assert staff_user.is_staff


def test_with_admin(admin_user):
    """Test with an admin user"""
    assert admin_user.is_superuser
```

### Pytest Markers

```python
import pytest


@pytest.mark.slow
def test_slow_operation():
    """Mark slow tests"""
    pass


@pytest.mark.integration
def test_integration():
    """Mark integration tests"""
    pass


# Run with: pytest -m "not slow"  # Skip slow tests
```

## Troubleshooting

### Tests Not Found

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH="$PWD/src:$PYTHONPATH"

# Or use quicktest which handles this
./quicktest
```

### Django Not Configured

```bash
# Ensure settings module is set
export DJANGO_SETTINGS_MODULE="tests.settings"

# Or use quicktest
./quicktest
```

### Import Errors

```bash
# Install in development mode
pip install -e .

# Or with test dependencies
pip install -e ".[test]"
```

### Coverage Not Working

```bash
# Ensure pytest-cov is installed
pip install pytest-cov

# Run with coverage
pytest --cov=trim
```

## Best Practices

### 1. Run Tests Frequently

```bash
# Quick test during development
./quicktest -f test_name -x

# Full test before commit
./quicktest -c
```

### 2. Write Tests First

Follow TDD principles:
1. Write failing test
2. Implement feature
3. Run test to verify

### 3. Test Multiple Scenarios

```python
def test_view_access_scenarios(self):
    """Test all access scenarios"""
    scenarios = [
        (None, 302),          # Anonymous -> redirect
        (user, 403),          # Regular user -> forbidden
        (staff_user, 200),    # Staff -> OK
        (admin_user, 200),    # Admin -> OK
    ]
    
    for test_user, expected_status in scenarios:
        with self.subTest(user=test_user):
            # Test logic here
            pass
```

### 4. Use Markers

```python
@pytest.mark.unit
def test_unit():
    """Fast unit test"""
    pass


@pytest.mark.integration
def test_integration():
    """Slower integration test"""
    pass
```

### 5. Parallel Testing

```bash
# Run tests in parallel for speed
./quicktest -p
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SETTINGS_MODULE` | `tests.settings` | Django settings module |
| `PYTHONPATH` | `src/` | Python import path |
| `PYTEST_ARGS` | `""` | Additional pytest arguments |
| `DJANGO_VERSION` | current | Override Django version |

## Scripts Reference

### quicktest Options

```
-h, --help          Show help message
-c, --coverage      Run with coverage report
-m, --multi         Run tests across all Django versions
-v, --version VER   Test specific Django version
-f, --filter TEST   Run specific test(s)
-p, --parallel      Run tests in parallel
-k, --keyword EXPR  Run tests matching keyword
-x, --exitfirst     Exit on first failure
-s, --stdout        Show print statements
--lf                Run last failed tests
--ff                Run failures first
```

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Tox Documentation](https://tox.wiki/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
