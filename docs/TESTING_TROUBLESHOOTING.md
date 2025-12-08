# Testing Troubleshooting Guide

This guide helps resolve common issues when running tests for `django-trim` across different Django versions.

## Quick Diagnosis

### Check Your Environment

```bash
# Check installed Django version
python -c "import django; print(django.get_version())"

# Check Python version
python --version

# List all installed packages
pip list | grep -i django
```

## Common Issues

### Issue: "pytest-django could not find a Django project (no manage.py file)"

**Problem:** pytest-django is looking for a Django project with manage.py but django-trim is a library, not a project.

**Symptoms:**
```
pytest-django could not find a Django project (no manage.py file could be found). 
You must explicitly add your Django project to the Python path to have it picked up.
```

**Solution:**

This is now fixed in the repository configuration, but if you encounter this:

1. **Check pytest.ini or pyproject.toml has:**
   ```ini
   [tool.pytest.ini_options]
   DJANGO_SETTINGS_MODULE = "tests.settings"
   django_find_project = false
   ```

2. **Ensure tests/ is a Python package:**
   ```bash
   # Create __init__.py if missing
   touch tests/__init__.py
   ```

3. **Set PYTHONPATH correctly:**
   ```bash
   # Include both src and root directory
   export PYTHONPATH="${PWD}/src:${PWD}"
   pytest
   ```

4. **For tox, check tox.ini has:**
   ```ini
   [testenv]
   setenv =
       PYTHONPATH = {toxinidir}/src:{toxinidir}
       DJANGO_SETTINGS_MODULE = tests.settings
   ```

5. **Verify Django settings exist:**
   ```bash
   # Should not error
   python -c "import tests.settings; print('OK')"
   ```

**Quick Fix:**
```bash
# Set up environment and run tests
export DJANGO_SETTINGS_MODULE=tests.settings
export PYTHONPATH="${PWD}/src:${PWD}"
pytest -v
```

### Issue: "Could not find a version that satisfies Django~=X.X.X"

**Problem:** The tox.ini or requirements file references a Django version that doesn't exist.

**Solution:**
```bash
# Check available Django versions
pip index versions Django

# Or visit PyPI directly
# https://pypi.org/project/Django/#history

# Update tox.ini to use version ranges instead of specific patches
# Good:  Django>=5.2,<5.3
# Bad:   Django~=5.2.99
```

**Latest Versions (Dec 2025):**
- Django 4.2: Latest is 4.2.27
- Django 5.0: Latest is 5.0.14
- Django 5.1: Latest is 5.1.15
- Django 5.2: Latest is 5.2.9
- Django 6.0: Latest is 6.0

### Issue: ImportError or Module Not Found

**Problem:** Test dependencies not installed or virtual environment issues.

**Solution:**
```bash
# Recreate the virtual environment
deactivate  # if in a venv
rm -rf .venv/ .tox/
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install test dependencies
pip install -e ".[test]"

# Or install from requirements
pip install -r requirements-test.txt

# Install a specific Django version
pip install "Django>=5.2,<5.3"
```

### Issue: Tox Environment Not Found

**Problem:** Python version not available on system.

**Solution:**
```bash
# List available tox environments
tox -l

# Skip missing Python versions
tox --skip-missing-interpreters

# Or install missing Python version (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv

# Using pyenv (recommended for multiple versions)
pyenv install 3.11.7
pyenv local 3.11.7
```

### Issue: Tests Pass Locally but Fail in CI

**Problem:** Environment differences between local and CI.

**Common Causes:**
1. Different Django versions installed
2. Missing dependencies
3. Database configuration differences
4. Timezone or locale differences

**Solution:**
```bash
# Match CI environment locally with tox
tox -e py311-dj52

# Check GitHub Actions workflow
cat .github/workflows/python-test.yml

# Run tests with same settings as CI
DJANGO_SETTINGS_MODULE=tests.settings pytest -v
```

### Issue: "No module named 'trim'"

**Problem:** Package not installed or PYTHONPATH not set.

**Solution:**
```bash
# Install in development mode
pip install -e .

# Or set PYTHONPATH manually
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Check if installed
pip show django-trim

# Verify imports work
python -c "import trim; print(trim.__file__)"
```

### Issue: Database Errors During Tests

**Problem:** Test database configuration issues.

**Solution:**
```bash
# Use SQLite for tests (default)
export DJANGO_SETTINGS_MODULE=tests.settings

# Clear test database
rm -f test_db.sqlite3

# Run tests with verbose output
pytest -v --ds=tests.settings

# Check if migrations are needed
python manage.py showmigrations
```

### Issue: Tox Environments Out of Sync

**Problem:** Tox cached environments have wrong dependencies.

**Solution:**
```bash
# Recreate all tox environments
tox -e clean
rm -rf .tox/

# Recreate specific environment
tox -e py311-dj52 --recreate

# Update dependencies without recreating
tox -e py311-dj52 --upgrade
```

### Issue: Tests Timeout or Hang

**Problem:** Background processes or infinite loops.

**Solution:**
```bash
# Run with timeout
pytest --timeout=300  # 5 minute timeout

# Use parallel execution carefully
pytest -n 4  # 4 parallel workers

# Or disable parallel execution
pytest -n 0

# Check for hanging processes
ps aux | grep python
```

### Issue: Coverage Report Errors

**Problem:** Coverage configuration or missing test runs.

**Solution:**
```bash
# Generate coverage with explicit source
pytest --cov=trim --cov-report=html --cov-report=term

# Combine coverage from multiple runs
coverage combine
coverage report
coverage html

# Check coverage configuration
cat pyproject.toml | grep -A 10 "\[tool.coverage"
```

## Django Version Specific Issues

### Django 4.2 LTS

**Compatible Python:** 3.8 - 3.12

**Common Issues:**
- Requires Python 3.8+ (won't work on 3.7)
- Some features deprecated, check warnings

**Solution:**
```bash
tox -e py311-dj42
# Or
pip install "Django>=4.2,<4.3"
```

### Django 5.0+

**Compatible Python:** 3.10 - 3.12

**Common Issues:**
- Requires Python 3.10+ (won't work on 3.8 or 3.9)
- Major version changes, check migration guide

**Solution:**
```bash
# Ensure Python 3.10+
python --version

# Install Django 5.0
pip install "Django>=5.0,<5.1"
```

### Django 5.2

**Compatible Python:** 3.10 - 3.12

**Common Issues:**
- Latest stable, may have newer features not in 4.2

**Solution:**
```bash
pip install "Django>=5.2,<5.3"
```

## Environment Setup Best Practices

### For Development

```bash
# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install in editable mode with test dependencies
pip install -e ".[test]"

# Run quick tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=trim --cov-report=html
```

### For Testing Multiple Versions

```bash
# Install tox
pip install tox

# List all test environments
tox -l

# Test all environments (takes time)
tox

# Test specific Django version
tox -e py311-dj52

# Test all Django versions with Python 3.11
tox -e py311-dj{42,50,51,52}
```

### For CI/CD

```bash
# Use matrix testing in GitHub Actions
# See .github/workflows/python-test.yml

# Test locally before pushing
tox -e py311-dj42,py311-dj52

# Or use quicktest script
./quicktest -v 5.2
```

## Performance Tips

### Speed Up Test Runs

```bash
# Use parallel execution (if tests support it)
pytest -n auto

# Run only failed tests
pytest --lf

# Run specific test file
pytest tests/test_models.py -v

# Skip slow tests
pytest -m "not slow"
```

### Reduce Tox Overhead

```bash
# Use skip-missing-interpreters
tox --skip-missing-interpreters

# Parallel tox runs (experimental)
tox -p auto

# Only rebuild changed environments
tox --skip-pkg-install
```

## Getting Help

If you encounter issues not covered here:

1. **Check GitHub Issues:** https://github.com/Strangemother/django-trim/issues
2. **Check Django Release Notes:** https://docs.djangoproject.com/en/stable/releases/
3. **Verify PyPI Versions:** https://pypi.org/project/Django/#history
4. **Run with verbose output:**
   ```bash
   pytest -vvv
   tox -vv -e py311-dj52
   ```

## Useful Commands Reference

```bash
# Quick environment check
python -c "import django; import trim; print(f'Django {django.get_version()}, trim OK')"

# Clean everything
rm -rf .tox/ .pytest_cache/ .coverage htmlcov/ **/__pycache__/

# Full test suite
tox && pytest --cov=trim --cov-report=html

# Quick test
pytest tests/ -v --ff

# Test specific pattern
pytest tests/ -k "test_models" -v
```

## Version Compatibility Matrix

| Python | Django 4.2 | Django 5.0 | Django 5.1 | Django 5.2 | Django 6.0 |
|--------|-----------|-----------|-----------|-----------|-----------|
| 3.8    | ✅         | ❌         | ❌         | ❌         | ❌         |
| 3.9    | ✅         | ❌         | ❌         | ❌         | ❌         |
| 3.10   | ✅         | ✅         | ✅         | ✅         | ✅         |
| 3.11   | ✅         | ✅         | ✅         | ✅         | ✅         |
| 3.12   | ✅         | ✅         | ✅         | ✅         | ✅         |
| 3.13   | ❌         | ❌         | ❌         | ❌         | ✅         |

✅ = Tested and supported  
❌ = Not compatible

---

**Last Updated:** December 2025  
**Django Versions:** 4.2.27, 5.0.14, 5.1.15, 5.2.9, 6.0
