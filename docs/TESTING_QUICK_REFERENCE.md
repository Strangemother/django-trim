# Django Version Testing - Quick Reference

One-page reference for testing `django-trim` across Django versions.

## Supported Versions (Dec 2025)

| Django | Latest | Python | Status |
|--------|--------|--------|--------|
| 4.2    | 4.2.27 | 3.8-3.12 | LTS ✅ |
| 5.0    | 5.0.14 | 3.10-3.12 | Stable |
| 5.1    | 5.1.15 | 3.10-3.12 | Stable |
| 5.2    | 5.2.9  | 3.10-3.12 | Stable |
| 6.0    | 6.0    | 3.10-3.13 | Latest ✅ |

## Quick Commands

```bash
# Quick test (current Django)
./quicktest

# Test specific Django version
./quicktest -v 4.2    # LTS
./quicktest -v 5.2    # Stable
./quicktest -v 6.0    # Latest

# Test all versions
tox

# Test specific combination
tox -e py311-dj52
```

## Common Issues & Fixes

### Issue: Version Not Found

```bash
# ❌ Error: Could not find Django~=5.2.99
# ✅ Fix: Use version ranges
pip install "Django>=5.2,<5.3"
```

### Issue: Import Error

```bash
# Install in dev mode
pip install -e ".[test]"
```

### Issue: Wrong Python Version

```bash
# Django 5.x needs Python 3.10+
python --version
# Upgrade if needed
```

### Issue: Tox Environment Broken

```bash
# Recreate environment
tox -e py311-dj52 --recreate
```

## Installation

```bash
# Development setup
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"

# Install specific Django version
pip install "Django>=5.2,<5.3"

# Verify
python -c "import django; print(django.get_version())"
```

## Test Matrix

```bash
# All Django with Python 3.11
tox -e py311-dj{42,50,51,52}

# All Python with Django 5.2
tox -e py{310,311,312}-dj52

# Specific test
pytest tests/test_models.py -v
```

## Version Ranges in Dependencies

```python
# pyproject.toml or requirements.txt
"Django>=4.2,<4.3"  # Django 4.2.x (LTS)
"Django>=5.2,<5.3"  # Django 5.2.x (Current)
```

## Environment Check

```bash
# Quick diagnostic
python -c "import django, trim; print(f'Django {django.get_version()}')"

# Full check
python --version
pip list | grep -i django
pytest --version
```

## CI/CD Matrix (GitHub Actions)

```yaml
# Tested combinations
python: [3.8, 3.9, 3.10, 3.11, 3.12]
django: [4.2, 5.0, 5.1, 5.2]
# Excluding incompatible: py38/py39 with django 5.x
```

## Links

+ **Full Docs:** [DJANGO_VERSIONS.md](../DJANGO_VERSIONS.md)
+ **Troubleshooting:** [TESTING_TROUBLESHOOTING.md](./TESTING_TROUBLESHOOTING.md)
+ **Django Releases:** https://pypi.org/project/Django/#history

## Tox Environments

```bash
# List all
tox -l

# Common ones
py311-dj42      # Recommended for compatibility (LTS)
py311-dj52      # Stable
py312-dj60      # Latest Django + Latest Python
py310-dj42      # Minimum for broad compatibility
```

## Performance

```bash
# Fast test (parallel)
pytest -n auto

# Specific test
pytest -k "test_models" -v

# Failed tests only
pytest --lf

# Skip missing interpreters
tox --skip-missing-interpreters
```

---

**Note:** Django 6.0 was released in December 2025. Test with both LTS (4.2) and latest (6.0) for best compatibility coverage.
