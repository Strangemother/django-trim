# django-trim Tests

This directory contains the test suite for django-trim.

## Quick Start

```bash
# Install test dependencies
pip install -e ".[test]"

# Run all tests
./quicktest

# Run with coverage
./quicktest -c
```

## Test Files

- **conftest.py** - Pytest configuration and fixtures
- **settings.py** - Django settings for testing
- **urls.py** - URL configuration for tests
- **test_trim_tests.py** - Tests for `trim.tests` module (mixin validation)
- **test_functional.py** - Functional tests
- **test_live.py** - Live model tests
- **test_rand.py** - Random utilities tests
- **test_urls.py** - URL utilities tests
- **test_updated_params.py** - Parameter update tests

## Available Fixtures

Defined in `conftest.py`:

- **user** - Regular test user
- **staff_user** - Staff user (is_staff=True)
- **admin_user** - Admin user (is_staff=True, is_superuser=True)
- **django_db_setup** - Database setup for tests

### Using Fixtures

```python
def test_with_user(user):
    """Test with a regular user fixture"""
    assert user.username == "testuser"


def test_with_staff(staff_user):
    """Test with a staff user fixture"""
    assert staff_user.is_staff
```

## Running Tests

### Quick Commands

```bash
# All tests
./quicktest

# With coverage
./quicktest -c

# Specific test
./quicktest -f test_mixin_order

# Parallel execution
./quicktest -p

# Multiple Django versions
./quicktest -m
```

### Pytest Directly

```bash
# All tests
pytest

# Specific file
pytest tests/test_trim_tests.py

# Specific test
pytest tests/test_trim_tests.py::TestMixinOrderValidation::test_correct_order_passes

# With coverage
pytest --cov=trim --cov-report=html
```

## Writing New Tests

### Structure

```python
import pytest
from django.test import TestCase
from trim import tests as trim_tests


class TestMyFeature:
    """Test suite for my feature"""
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        assert True
    
    @pytest.mark.slow
    def test_slow_operation(self):
        """Mark slow tests"""
        pass


class TestDjangoFeature(TestCase):
    """Django TestCase for database tests"""
    
    def test_with_db(self):
        """Test requiring database"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user('test', 'test@example.com')
        assert user.username == 'test'
```

### Best Practices

1. **One test, one assertion** - Focus tests on single behaviors
2. **Descriptive names** - `test_mixin_order_correct_when_auth_before_view`
3. **Use fixtures** - Reuse common setup code
4. **Mark slow tests** - Use `@pytest.mark.slow`
5. **Document complex tests** - Add docstrings explaining what's tested

## Test Markers

Available markers (defined in `pyproject.toml`):

- **@pytest.mark.slow** - Slow-running tests
- **@pytest.mark.integration** - Integration tests
- **@pytest.mark.unit** - Unit tests

### Using Markers

```python
@pytest.mark.slow
def test_slow_operation():
    pass

# Run: pytest -m "not slow"  # Skip slow tests
```

## Coverage

Coverage settings are in `pyproject.toml`:

- **Source**: `src/trim`
- **Omit**: Tests, migrations, pycache
- **Branch coverage**: Enabled
- **Reports**: HTML, XML, terminal

View HTML coverage report:

```bash
./quicktest -c
open htmlcov/index.html
```

## Multi-Version Testing

Test across multiple Django versions:

```bash
# All versions with tox
./quicktest -m

# Specific version
./quicktest -v 4.2
./quicktest -v 5.0

# Specific environment
tox -e py311-django42
```

## Troubleshooting

### Import Errors

```bash
# Ensure django-trim is installed in dev mode
pip install -e .
```

### Django Not Configured

```bash
# Set environment variable
export DJANGO_SETTINGS_MODULE="tests.settings"

# Or use quicktest (does this automatically)
./quicktest
```

### Tests Not Found

```bash
# Ensure correct path
export PYTHONPATH="$PWD/src:$PYTHONPATH"

# Or use quicktest
./quicktest
```

## Resources

- [../docs/TESTING.md](../docs/TESTING.md) - Complete testing guide
- [../docs/testing.md](../docs/testing.md) - Testing utilities documentation
- [pytest documentation](https://docs.pytest.org/)
- [Django testing](https://docs.djangoproject.com/en/stable/topics/testing/)
