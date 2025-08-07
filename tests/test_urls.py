
import unittest
from unittest.mock import patch

from trim import urls

class TestUrls(unittest.TestCase):
    """Unit tests for URL-related functionality."""

    @patch('trim.urls.reverse')
    @patch('trim.urls.absolutify')
    def test_absolute_reverse(self, mock_absolutify, mock_reverse):
        """Test that absolute_reverse returns the correct absolute URL."""
        # Setup
        mock_reverse.return_value = '/some/path/'
        request = 'dummy_request'
        # Expected: Absolute URL should be constructed correctly
        expected_url = 'http://example.com/some/path/'
        mock_absolutify.return_value = expected_url
        
        # Result
        name = 'some_view_name',
        args = ()
        result = urls.absolute_reverse(request, name, *args)
        
        # Check if the result matches expected URL
        self.assertEqual(result, expected_url)
        mock_reverse.assert_called_once_with(name, args=args)
        mock_absolutify.assert_called_once_with(request, '/some/path/')
    
    def test_absolutify(self):
        """Test that absolutify constructs the correct absolute URL."""
        class MockRequest:
            scheme = 'http'
            get_host = lambda self: 'example.com'
        
        request = MockRequest()
        relative_url = '/some/path/'
        # Expected: Absolute URL should be constructed correctly
        expected_url = 'http://example.com/some/path/'
        # Result
        result = urls.absolutify(request, relative_url)
        # Check if the result matches expected URL
        self.assertEqual(result, expected_url)

    @patch('trim.urls.path')
    @patch('trim.urls.staticfiles_storage')
    def test_favicon_path(self, mock_path, mock_staticfiles_storage):
        """Test that favicon_path returns the correct path."""
        # Expected: Favicon path should be '/static/favicon.ico'
        expected_path = '/static/favicon.ico'
        # Result
        result = urls.favicon_path()
        # Check if the result matches expected path
        self.assertEqual(result, expected_path)