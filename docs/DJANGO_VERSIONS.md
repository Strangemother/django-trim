# Django Version Testing Reference

Quick reference for testing django-trim against different Django versions.

## Supported Versions (December 2025)

Based on [Django Release Schedule](https://www.djangoproject.com/download/):

| Version | Status | Latest Release | Support Until | Notes |
|---------|--------|----------------|--------------|-------|
| **3.2** | LTS | 3.2.25 | April 2024 | Extended support ended - not tested |
| **4.2** | LTS | 4.2.27 | April 2026 | Long Term Support - most stable |
| **5.0** | Stable | 5.0.14 | April 2025 | Stable release |
| **5.1** | Stable | 5.1.15 | December 2025 | Stable release |
| **5.2** | Stable | 5.2.9 | August 2026 | Stable release |
| **6.0** | Latest | 6.0 | December 2025 | Latest major release |

**Note:** Django versions follow semantic versioning. The complete list of all Django releases from 1.1.3 to 6.0 is available on [PyPI](https://pypi.org/project/Django/#history). The `django-trim` project focuses testing on actively maintained versions (4.2+).

## Quick Test Commands

### Using quicktest

```bash
# Test with current environment Django version
./quicktest

# Test specific Django version (creates isolated venv)
./quicktest -v 4.2    # Django 4.2 LTS (recommended)
./quicktest -v 5.0    # Django 5.0
./quicktest -v 5.1    # Django 5.1
./quicktest -v 5.2    # Django 5.2
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
tox -e py310-dj42     # Python 3.10, Django 4.2 LTS
tox -e py311-dj52     # Python 3.11, Django 5.2
tox -e py312-dj60     # Python 3.12, Django 6.0 (latest)

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

### Django 5.2 (Stable)
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

| Django Version | Minimum Python | Maximum Python | Notes |
|---------------|---------------|---------------|-------|
| 3.2 LTS       | 3.6           | 3.10          | Not actively tested |
| 4.2 LTS       | 3.8           | 3.12          | Recommended for production |
| 5.0           | 3.10          | 3.12          | Stable |
| 5.1           | 3.10          | 3.12          | Stable |
| 5.2           | 3.10          | 3.12          | Stable |
| 6.0           | 3.10          | 3.13          | Latest |

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
# Test on latest (6.0)
./quicktest -v 6.0 -f test_my_feature

# Test on stable (5.2)
./quicktest -v 5.2 -f test_my_feature

# Test on LTS (4.2) - recommended for compatibility
./quicktest -v 4.2 -f test_my_feature
```

### CI/CD Testing
```bash
# GitHub Actions automatically tests:
# - Python 3.8, 3.9 with Django 4.2
# - Python 3.10, 3.11, 3.12 with Django 4.2, 5.0, 5.1, 5.2, 6.0
```

## Troubleshooting

> **📖 Full Troubleshooting Guide:** See [TESTING_TROUBLESHOOTING.md](./TESTING_TROUBLESHOOTING.md) for comprehensive solutions to common testing issues.

### Version Not Found
```bash
# Error: Could not find a version that satisfies Django~=X.X.X
# Solution: Use version ranges instead of specific patches
# Good: Django>=5.2,<5.3
# Bad:  Django~=5.2.99

# Check available versions on PyPI
pip index versions Django

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
- **Latest stable** (6.0) has newest features, monitor for stability
- **Stable versions** (5.2, 5.1, 5.0) balance features and stability
- **Older versions** (3.2 and earlier) are no longer tested but may work
- **Pre-releases** (rc1, beta, alpha) are not included in automated testing
- Django has released versions from 1.1.3 through 6.0 as of December 2025
- Focus testing on actively supported Django versions to ensure compatibility

## All Available Django Versions

For reference, Django has released the following versions (complete list as of Dec 2025):

**Django 1.x:** 1.1.3, 1.1.4, 1.2-1.2.7, 1.3-1.3.7, 1.4-1.4.22, 1.5-1.5.12, 1.6-1.6.11, 1.7-1.7.11, 1.8-1.8.19, 1.9-1.9.13, 1.10-1.10.8, 1.11-1.11.29

**Django 2.x:** 2.0-2.0.13, 2.1-2.1.15, 2.2-2.2.28 (LTS)

**Django 3.x:** 3.0-3.0.14, 3.1-3.1.14, 3.2-3.2.25 (LTS)

**Django 4.x:** 4.0-4.0.10, 4.1-4.1.13, 4.2-4.2.27 (LTS)

**Django 5.x:** 5.0-5.0.14, 5.1-5.1.15, 5.2-5.2.9

**Django 6.x:** 6.0 (latest)

See [PyPI Django History](https://pypi.org/project/Django/#history) for the complete release timeline.

## Resources

- [Django Download Page](https://www.djangoproject.com/download/)
- [Django Release Notes](https://docs.djangoproject.com/en/stable/releases/)
- [PyPI Django Releases](https://pypi.org/project/Django/#history)
- [Django Supported Versions](https://www.djangoproject.com/download/#supported-versions)
