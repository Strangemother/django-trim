"""
Pytest configuration and fixtures for django-trim tests.

This file is automatically loaded by pytest and sets up Django for testing.
"""
import os
import sys
import django
import pytest
from pathlib import Path

# Add src to path so we can import trim
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

# Setup Django
django.setup()


@pytest.fixture(scope="session")
def django_db_setup():
    """
    Setup test database.
    Uses in-memory SQLite for speed.
    """
    from django.conf import settings
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }


@pytest.fixture
def user(db, django_user_model):
    """Create a test user."""
    return django_user_model.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )


@pytest.fixture
def staff_user(db, django_user_model):
    """Create a staff user."""
    return django_user_model.objects.create_user(
        username="staffuser",
        email="staff@example.com",
        password="staffpass123",
        is_staff=True
    )


@pytest.fixture
def admin_user(db, django_user_model):
    """Create an admin user."""
    return django_user_model.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="adminpass123",
        is_staff=True,
        is_superuser=True
    )

django.setup()
