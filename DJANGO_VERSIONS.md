# Django Version Testing Reference

Quick reference for testing django-trim against different Django versions.

## Supported Versions (December 2025)

Based on [Django Release Schedule](https://www.djangoproject.com/download/):

| Version | Status | Support Until | Notes |
|---------|--------|--------------|-------|
| **4.2** | LTS | April 2026 | Long Term Support - most stable |
| **5.0** | Stable | April 2025 | Stable release |
| **5.1** | Stable | August 2025 | Stable release |
| **5.2** | Current | December 2025 | Current stable |
| **6.0** | Latest | December 2025 | Latest release |

## Quick Test Commands

### Using quicktest

```bash
# Test with current environment Django version
./quicktest

# Test specific Django version (creates isolated venv)
./quicktest -v 4.2    # Django 4.2 LTS
./quicktest -v 5.0    # Django 5.0
./quicktest -v 5.1    # Django 5.1
./quicktest -v 5.2    # Django 5.2 (current)
./quicktest -v 6.0    # Django 6.0 (latest)

# Test all versions with tox
./quicktest -m
```

### Using tox directly

```bash
# List all available environments
tox -l

# Test all environments
tox

# Test specific Python + Django combination
tox -e py310-dj42     # Python 3.10, Django 4.2
tox -e py311-dj52     # Python 3.11, Django 5.2
tox -e py312-dj60     # Python 3.12, Django 6.0

# Test all Django versions with specific Python
tox -e py311-dj{42,50,51,52,60}

# Test specific Django with all Python versions
tox -e py{310,311,312}-dj52
```

## Available tox Environments

### Django 4.2 LTS
```
py38-dj42   # Python 3.8 + Django 4.2
py39-dj42   # Python 3.9 + Django 4.2
py310-dj42  # Python 3.10 + Django 4.2
py311-dj42  # Python 3.11 + Django 4.2
py312-dj42  # Python 3.12 + Django 4.2
```

### Django 5.0
```
py310-dj50  # Python 3.10 + Django 5.0
py311-dj50  # Python 3.11 + Django 5.0
py312-dj50  # Python 3.12 + Django 5.0
```

### Django 5.1
```
py310-dj51  # Python 3.10 + Django 5.1
py311-dj51  # Python 3.11 + Django 5.1
py312-dj51  # Python 3.12 + Django 5.1
```

### Django 5.2 (Current)
```
py310-dj52  # Python 3.10 + Django 5.2
py311-dj52  # Python 3.11 + Django 5.2
py312-dj52  # Python 3.12 + Django 5.2
```

### Django 6.0 (Latest)
```
py310-dj60  # Python 3.10 + Django 6.0
py311-dj60  # Python 3.11 + Django 6.0
py312-dj60  # Python 3.12 + Django 6.0
```

## Python Version Requirements

| Django Version | Minimum Python | Maximum Python |
|---------------|---------------|---------------|
| 4.2 LTS       | 3.8           | 3.12          |
| 5.0           | 3.10          | 3.12          |
| 5.1           | 3.10          | 3.12          |
| 5.2           | 3.10          | 3.12          |
| 6.0           | 3.10          | 3.13          |

## Common Workflows

### Before Committing
```bash
# Quick test with your current Django
./quicktest -c

# Test with LTS version
./quicktest -v 4.2
```

### Before Release
```bash
# Test all supported versions
./quicktest -m

# Or with tox
tox
```

### Testing a Feature
```bash
# Test on current stable (5.2)
./quicktest -v 5.2 -f test_my_feature

# Test on LTS (4.2)
./quicktest -v 4.2 -f test_my_feature

# Test on latest (6.0)
./quicktest -v 6.0 -f test_my_feature
```

### CI/CD Testing
```bash
# GitHub Actions automatically tests:
# - Python 3.8, 3.9 with Django 4.2
# - Python 3.10, 3.11, 3.12 with Django 4.2, 5.0, 5.1, 5.2, 6.0
```

## Troubleshooting

### Version Not Found
```bash
# Error: Could not find a version that satisfies Django~=X.X.X
# Solution: Check if version exists on PyPI
pip search Django | grep "^Django "

# Or visit https://pypi.org/project/Django/#history
```

### Environment Conflicts
```bash
# Clear tox environments
tox -e clean
rm -rf .tox/

# Recreate specific environment
tox -e py311-dj52 --recreate
```

### Python Version Missing
```bash
# Install missing Python version (Ubuntu/Debian)
sudo apt-get install python3.10 python3.10-venv

# Or use pyenv
pyenv install 3.10.13
pyenv install 3.11.7
pyenv install 3.12.1
```

## Installation Notes

### Install Test Dependencies
```bash
# Install with all test dependencies
pip install -e ".[test]"

# Or install specific Django version
pip install -e ".[test]" "Django~=5.2.9"
```

### Install Tox
```bash
pip install tox
```

## Notes

- **LTS versions** (4.2) are recommended for production
- **Current stable** (5.2) balances features and stability
- **Latest** (6.0) has newest features but may have bugs
- **Older versions** (3.2, 4.1) are no longer tested but may work
- **Pre-releases** (rc1, beta, alpha) are not included in automated testing

## Resources

- [Django Download Page](https://www.djangoproject.com/download/)
- [Django Release Notes](https://docs.djangoproject.com/en/stable/releases/)
- [PyPI Django Releases](https://pypi.org/project/Django/#history)
- [Django Supported Versions](https://www.djangoproject.com/download/#supported-versions)
