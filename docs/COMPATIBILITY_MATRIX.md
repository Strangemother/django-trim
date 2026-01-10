# Python & Django Compatibility Matrix

**django-trim v0.4.2** compatibility:

| Python | Django 4.2 LTS | Django 5.0 | Django 5.1 | Django 5.2 |
|--------|:--------------:|:----------:|:----------:|:----------:|
| 3.8    | ✅             | ❌         | ❌         | ❌         |
| 3.9    | ✅             | ❌         | ❌         | ❌         |
| 3.10   | ✅             | ✅         | ✅         | ✅         |
| 3.11   | ✅             | ✅         | ✅         | ✅         |
| 3.12   | ✅             | ✅         | ✅         | ✅         |
| 3.13   | ✅             | ✅         | ✅         | ✅         |
| 3.14   | ✅             | ✅         | ✅         | ✅         |

**Legend:** ✅ Supported and tested | ❌ Not compatible

## Test Environments

| Python | Django 4.2 | Django 5.0 | Django 5.1 | Django 5.2 |
|--------|------------|------------|------------|------------|
| 3.8    | `py38-dj42` | — | — | — |
| 3.9    | `py39-dj42` | — | — | — |
| 3.10   | `py310-dj42` | `py310-dj50` | `py310-dj51` | `py310-dj52` |
| 3.11   | `py311-dj42` | `py311-dj50` | `py311-dj51` | `py311-dj52` |
| 3.12   | `py312-dj42` | `py312-dj50` | `py312-dj51` | `py312-dj52` |
| 3.13   | `py313-dj42` | `py313-dj50` | `py313-dj51` | `py313-dj52` |
| 3.14   | `py314-dj42` | `py314-dj50` | `py314-dj51` | `py314-dj52` |

**Total:** 24 environment combinations tested in CI/CD

## Quick Recommendations

- **Production:** Python 3.10+ with Django 4.2 LTS
- **New projects:** Python 3.11/3.12 with Django 4.2 LTS  
- **Latest features:** Python 3.12 with Django 5.2

## Python Version Notes

- **3.8:** End of life (Oct 2024) - security risk, upgrade recommended
- **3.9:** End of life (Oct 2025) - upgrade recommended
- **3.10:** Active until Oct 2026 - good for production
- **3.11:** Active until Oct 2027 - good for production  
- **3.12:** Active until Oct 2028 - recommended
- **3.13:** Active until Oct 2029 - latest stable
- **3.14:** Active until Oct 2030 - bleeding edge

## Django Version Notes

- **4.2 LTS:** Supported until April 2026 - recommended for production
- **5.0:** Supported until April 2025 - requires Python 3.10+
- **5.1:** Supported until December 2025 - requires Python 3.10+
- **5.2:** Supported until August 2026 - requires Python 3.10+

## Testing

See [DJANGO_VERSIONS.md](../DJANGO_VERSIONS.md) for testing commands and workflows.
