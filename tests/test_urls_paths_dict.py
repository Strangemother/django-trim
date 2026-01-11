"""
Dedicated test suite for paths_dict function.
This function is complex enough to warrant its own test file.
"""
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from django.views.generic import ListView, CreateView

from trim import urls


class TestPathsDict(TestCase):
    """Test suite for paths_dict function."""

    @patch("trim.urls.paths")
    @patch("trim.urls.clean_str")
    def test_calls_clean_str_on_prefixes(self, mock_clean, mock_paths):
        """Test clean_str is called on all prefix parameters."""
        # Setup
        mock_clean.side_effect = lambda x: x or ""
        mock_paths.return_value = []
        mock_views = Mock()
        # Execute
        urls.paths_dict(
            mock_views,
            {},
            view_prefix="Product",
            url_pattern_prefix="api/",
            url_name_prefix="prod-",
        )
        # Assert
        self.assertEqual(mock_clean.call_count, 3)

    @patch("trim.urls.paths")
    def test_returns_result_from_paths(self, mock_paths):
        """Test paths_dict returns the result from paths()."""
        # Setup
        mock_paths.return_value = ["result"]
        mock_views = Mock()
        # Execute
        result = urls.paths_dict(mock_views, {})
        # Assert
        self.assertEqual(result, ["result"])

    @patch("trim.urls.paths")
    def test_patterns_defaults_to_empty_dict(self, mock_paths):
        """Test patterns parameter defaults to empty dict."""
        # Setup
        mock_paths.return_value = []
        mock_views = Mock()
        # Execute
        urls.paths_dict(mock_views, None)
        # Assert - should not raise error
        mock_paths.assert_called_once()

    @patch("trim.urls.paths")
    def test_merges_kwargs_into_patterns(self, mock_paths):
        """Test **kw params are merged into patterns dict."""
        # Setup
        mock_paths.return_value = []
        mock_views = Mock()
        mock_views.ListView = Mock()
        patterns = {"CreateView": ("create", "new/")}
        # Execute
        urls.paths_dict(
            mock_views, patterns, DetailView=("detail", "<pk>/")
        )
        # Assert - both patterns and kwargs should be processed
        call_arg = mock_paths.call_args[0][0]
        self.assertEqual(len(call_arg), 2)

    @patch("trim.urls.paths")
    def test_builds_class_name_with_view_prefix(self, mock_paths):
        """Test view_prefix is prepended to pattern keys."""
        # Setup
        mock_paths.return_value = []
        mock_views = Mock()
        mock_views.ProductListView = Mock()
        # Execute
        urls.paths_dict(
            mock_views, {"ListView": ("list", "")}, view_prefix="Product"
        )
        # Assert - should call getattr with 'ProductListView'
        self.assertTrue(hasattr(mock_views, "ProductListView"))

    @patch("trim.urls.paths")
    def test_raises_attribute_error_when_view_missing(self, mock_paths):
        """Test AttributeError raised when view not found and ignore=False."""
        # Setup
        mock_paths.return_value = []
        mock_views = Mock(spec=[])
        # Execute & Assert
        with self.assertRaises(AttributeError):
            urls.paths_dict(
                mock_views,
                {"ListView": ("list", "")},
                ignore_missing_views=False,
            )

    @patch("trim.urls.paths")
    def test_continues_when_view_missing_and_ignore_true(self, mock_paths):
        """Test continues silently when view missing and ignore=True."""
        # Setup
        mock_paths.return_value = []
        mock_views = Mock(spec=[])
        # Execute
        result = urls.paths_dict(
            mock_views, {"ListView": ("list", "")}, ignore_missing_views=True
        )
        # Assert - should not raise, returns empty result
        self.assertEqual(result, [])

    @patch("trim.urls.paths")
    @patch("trim.urls.inspect.getmro")
    @patch("trim.urls.MAPPED_CLASS", {"ListView": "list"})
    def test_converts_string_url_to_tuple(self, mock_getmro, mock_paths):
        """Test string URL gets converted to tuple with MAPPED_CLASS lookup."""
        # Setup
        mock_paths.return_value = []
        mock_view = Mock()
        mock_getmro.return_value = (mock_view, ListView)
        mock_views = Mock()
        mock_views.ListView = mock_view
        # Execute
        urls.paths_dict(mock_views, {"ListView": ""})
        # Assert
        call_arg = mock_paths.call_args[0][0]
        self.assertEqual(len(call_arg), 1)
        fname, entry = call_arg[0]
        self.assertEqual(entry[0], "")  # URL

    @patch("trim.urls.paths")
    def test_unpacks_solution_tuple(self, mock_paths):
        """Test solution tuple is unpacked into path_name, url, extra."""
        # Setup
        mock_paths.return_value = []
        mock_view = Mock()
        mock_views = Mock()
        mock_views.ListView = mock_view
        # Execute
        urls.paths_dict(
            mock_views, {"ListView": ("list", "items/", {"extra": "data"})}
        )
        # Assert
        call_arg = mock_paths.call_args[0][0]
        fname, entry = call_arg[0]
        self.assertEqual(entry[0], "items/")  # URL
        self.assertEqual(entry[2], {"extra": "data"})  # extra

    @patch("trim.urls.paths")
    def test_applies_url_pattern_prefix(self, mock_paths):
        """Test url_pattern_prefix is prepended to URL."""
        # Setup
        mock_paths.return_value = []
        mock_view = Mock()
        mock_views = Mock()
        mock_views.ListView = mock_view
        # Execute
        urls.paths_dict(
            mock_views,
            {"ListView": ("list", "items/")},
            url_pattern_prefix="api/",
        )
        # Assert
        call_arg = mock_paths.call_args[0][0]
        fname, entry = call_arg[0]
        self.assertEqual(entry[0], "api/items/")

    @patch("trim.urls.paths")
    def test_applies_url_name_prefix(self, mock_paths):
        """Test url_name_prefix is prepended to path name."""
        # Setup
        mock_paths.return_value = []
        mock_view = Mock()
        mock_views = Mock()
        mock_views.ListView = mock_view
        # Execute
        urls.paths_dict(
            mock_views, {"ListView": ("list", "")}, url_name_prefix="product-"
        )
        # Assert
        call_arg = mock_paths.call_args[0][0]
        fname, entry = call_arg[0]
        self.assertEqual(fname, "product-list")

    @patch("trim.urls.paths")
    def test_handles_multiple_urls_as_tuple(self, mock_paths):
        """Test URL as tuple creates multiple entries."""
        # Setup
        mock_paths.return_value = []
        mock_view = Mock()
        mock_views = Mock()
        mock_views.ListView = mock_view
        # Execute
        urls.paths_dict(
            mock_views, {"ListView": ("list", ("", "items/"))}
        )
        # Assert
        call_arg = mock_paths.call_args[0][0]
        self.assertEqual(len(call_arg), 2)  # Two URLs

    @patch("trim.urls.paths")
    def test_safe_prefix_adds_part_name_to_duplicate(self, mock_paths):
        """Test safe_prefix=True prepends part_name to avoid collisions."""
        # Setup
        mock_paths.return_value = []
        mock_view = Mock()
        mock_views = Mock()
        mock_views.ListView = mock_view
        # Execute
        urls.paths_dict(
            mock_views, {"ListView": ("list", "")}, safe_prefix=True
        )
        # Assert
        call_arg = mock_paths.call_args[0][0]
        fname, entry = call_arg[0]
        self.assertTrue(fname.startswith("listview-"))

    @patch("trim.urls.paths")
    def test_forwards_extra_params_to_paths(self, mock_paths):
        """Test extra params in solution are forwarded."""
        # Setup
        mock_paths.return_value = []
        mock_view = Mock()
        mock_views = Mock()
        mock_views.ListView = mock_view
        extra_dict = {"permission": "view"}
        # Execute
        urls.paths_dict(
            mock_views, {"ListView": ("list", "", extra_dict)}
        )
        # Assert
        call_arg = mock_paths.call_args[0][0]
        fname, entry = call_arg[0]
        self.assertIn(extra_dict, entry)
