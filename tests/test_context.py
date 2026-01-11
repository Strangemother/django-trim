"""
Test trim.context module.

Tests the context processor functionality for Django templates.
"""

from django.test import RequestFactory, TestCase, override_settings
from django.urls import path, include
from django.http import HttpResponse


def dummy_view(request):
    """Dummy view for URL testing."""
    return HttpResponse("OK")


# Test URL patterns with app namespace
test_urlpatterns = [
    path('test-app/', include(([
        path('page/', dummy_view, name='test_page'),
    ], 'testapp'))),
    path('no-app/', dummy_view, name='no_app_page'),
]


@override_settings(ROOT_URLCONF='tests.test_context')
class AppNameContextProcessorTest(TestCase):
    """Test the appname context processor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.factory = RequestFactory()
    
    def test_appname_with_app_namespace(self):
        """Test appname returns app_name when URL has an app namespace."""
        from trim.context import appname
        
        request = self.factory.get('/test-app/page/')
        request.path = '/test-app/page/'
        
        result = appname(request)
        self.assertIsInstance(result, dict)
        self.assertIn('appname', result)
        self.assertEqual(result['appname'], 'testapp')
    
    def test_appname_without_app_namespace(self):
        """Test appname returns empty string when URL has no app namespace."""
        from trim.context import appname
        
        request = self.factory.get('/no-app/')
        request.path = '/no-app/'
        
        result = appname(request)
        self.assertIsInstance(result, dict)
        self.assertIn('appname', result)
        self.assertEqual(result['appname'], '')
    
    def test_appname_returns_dict(self):
        """Test that appname always returns a dictionary."""
        from trim.context import appname
        
        request = self.factory.get('/test-app/page/')
        request.path = '/test-app/page/'
        
        result = appname(request)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 1)


# Export urlpatterns for override_settings to work
urlpatterns = test_urlpatterns
