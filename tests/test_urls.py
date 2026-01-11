import unittest
from unittest.mock import patch

from trim import urls


class TestUrls(unittest.TestCase):
    """Unit tests for URL-related functionality."""

    @patch("trim.urls.reverse")
    @patch("trim.urls.absolutify")
    def test_absolute_reverse(self, mock_absolutify, mock_reverse):
        """Test that absolute_reverse returns the correct absolute URL."""
        # Setup
        mock_reverse.return_value = "/some/path/"
        request = "dummy_request"
        # Expected: Absolute URL should be constructed correctly
        expected_url = "http://example.com/some/path/"
        mock_absolutify.return_value = expected_url

        # Result
        name = ("some_view_name",)
        args = ()
        result = urls.absolute_reverse(request, name, *args)

        # Check if the result matches expected URL
        self.assertEqual(result, expected_url)
        mock_reverse.assert_called_once_with(name, args=args)
        mock_absolutify.assert_called_once_with(request, "/some/path/")

    def test_absolutify(self):
        """Test that absolutify constructs the correct absolute URL."""

        class MockRequest:
            scheme = "http"
            get_host = lambda self: "example.com"

        request = MockRequest()
        relative_url = "/some/path/"
        # Expected: Absolute URL should be constructed correctly
        expected_url = "http://example.com/some/path/"
        # Result
        result = urls.absolutify(request, relative_url)
        # Check if the result matches expected URL
        self.assertEqual(result, expected_url)

    @patch("trim.urls.staticfiles_storage")
    @patch("trim.urls.path")
    def test_favicon_path(self, mock_path, mock_staticfiles_storage):
        """Test that favicon_path returns the correct path."""
        # Expected: Favicon path should be '/static/favicon.ico'
        expected_path = "/static/favicon.ico"
        mock_path.return_value = expected_path
        # Result
        result = urls.favicon_path()
        # Check if the result matches expected path
        self.assertEqual(result, expected_path)

    def test_clean_str_with_none(self):
        """Test clean_str returns empty string for None."""
        self.assertEqual(urls.clean_str(None), "")

    def test_clean_str_with_false(self):
        """Test clean_str returns empty string for False."""
        self.assertEqual(urls.clean_str(False), "")

    def test_clean_str_with_string(self):
        """Test clean_str returns the string unchanged."""
        self.assertEqual(urls.clean_str("hello"), "hello")

    def test_clean_str_with_empty_string(self):
        """Test clean_str returns empty string unchanged."""
        self.assertEqual(urls.clean_str(""), "")

    @patch("trim.urls.paths")
    @patch("trim.urls.django_include")
    def test_path_includes_single_name(self, mock_include, mock_paths):
        """Test path_includes with single string name."""
        # Setup
        mock_paths.return_value = "result"
        # Execute
        result = urls.path_includes("products")
        # Assert
        expected = (
            ("products", ("products/", mock_include.return_value)),
        )
        mock_include.assert_called_once_with("products.urls")
        mock_paths.assert_called_once_with(expected)
        self.assertEqual(result, "result")

    @patch("trim.urls.paths")
    @patch("trim.urls.django_include")
    def test_path_includes_multiple_names(self, mock_include, mock_paths):
        """Test path_includes with multiple names."""
        # Setup
        mock_paths.return_value = "result"
        # Execute
        result = urls.path_includes("products", "orders")
        # Assert
        self.assertEqual(mock_include.call_count, 2)
        mock_include.assert_any_call("products.urls")
        mock_include.assert_any_call("orders.urls")
        self.assertEqual(result, "result")

    @patch("trim.urls.paths")
    @patch("trim.urls.django_include")
    def test_path_includes_with_nested_tuple(self, mock_include, mock_paths):
        """Test path_includes flattens nested tuples."""
        # Setup
        mock_paths.return_value = "result"
        # Execute
        result = urls.path_includes(("products", "orders"))
        # Assert
        self.assertEqual(mock_include.call_count, 2)
        mock_include.assert_any_call("products.urls")
        mock_include.assert_any_call("orders.urls")
        self.assertEqual(result, "result")

    @patch("trim.urls.paths")
    @patch("trim.urls.django_include")
    def test_path_includes_pair_with_string(self, mock_include, mock_paths):
        """Test path_includes_pair auto-generates URL from string."""
        # Setup
        mock_paths.return_value = "result"
        # Execute
        result = urls.path_includes_pair("products")
        # Assert
        expected = (("products", ("products/", mock_include.return_value)),)
        mock_include.assert_called_once_with("products.urls")
        mock_paths.assert_called_once_with(expected)
        self.assertEqual(result, "result")

    @patch("trim.urls.paths")
    @patch("trim.urls.django_include")
    def test_path_includes_pair_with_custom_url(self, mock_include, mock_paths):
        """Test path_includes_pair uses custom URL from tuple."""
        # Setup
        mock_paths.return_value = "result"
        # Execute
        result = urls.path_includes_pair(("trim.account", "account/"))
        # Assert
        expected = (("trim.account", ("account/", mock_include.return_value)),)
        mock_include.assert_called_once_with("trim.account.urls")
        mock_paths.assert_called_once_with(expected)
        self.assertEqual(result, "result")

    @patch("trim.urls.paths")
    @patch("trim.urls.django_include")
    def test_path_includes_pair_mixed(self, mock_include, mock_paths):
        """Test path_includes_pair with mixed string and tuple."""
        # Setup
        mock_paths.return_value = "result"
        # Execute
        result = urls.path_includes_pair("file", ("trim.account", "account/"))
        # Assert
        self.assertEqual(mock_include.call_count, 2)
        mock_include.assert_any_call("file.urls")
        mock_include.assert_any_call("trim.account.urls")
        self.assertEqual(result, "result")

    @patch("trim.urls.paths")
    @patch("trim.urls.django_include")
    def test_path_include_basic(self, mock_include, mock_paths):
        """Test path_include adds trailing slash to URL."""
        # Setup
        mock_paths.return_value = "result"
        # Execute
        result = urls.path_include("products")
        # Assert
        expected = (("products", ("products/", mock_include.return_value)),)
        mock_include.assert_called_once_with("products.urls")
        mock_paths.assert_called_once_with(expected)
        self.assertEqual(result, "result")

    @patch("trim.urls.paths")
    @patch("trim.urls.django_include")
    def test_path_include_with_custom_module(self, mock_include, mock_paths):
        """Test path_include uses custom module."""
        # Setup
        mock_paths.return_value = "result"
        # Execute
        result = urls.path_include("mythings/", "products.urls")
        # Assert
        expected = (("ythings/", ("mythings/", mock_include.return_value)),)
        mock_include.assert_called_once_with("products.urls")
        mock_paths.assert_called_once_with(expected)
        self.assertEqual(result, "result")

    @patch("trim.urls.paths")
    @patch("trim.urls.django_include")
    def test_path_include_with_custom_name(self, mock_include, mock_paths):
        """Test path_include uses custom path name."""
        # Setup
        mock_paths.return_value = "result"
        # Execute
        result = urls.path_include("mythings/", "products.urls", "items")
        # Assert
        expected = (("items", ("mythings/", mock_include.return_value)),)
        mock_include.assert_called_once_with("products.urls")
        mock_paths.assert_called_once_with(expected)
        self.assertEqual(result, "result")

    @patch("trim.urls.paths_less")
    @patch("trim.urls.trim_names")
    def test_paths_default_builds_patterns(self, mock_trim_names, mock_paths_less):
        """Test paths_default builds patterns dict from views."""
        # Setup
        mock_trim_names.get_url.side_effect = ["", "new/", "<str:pk>/"]
        mock_paths_less.return_value = "result"
        views_list = ("list", "create", "detail")
        # Execute
        result = urls.paths_default("mock_views", "mock_models", views=views_list)
        # Assert
        self.assertEqual(mock_trim_names.get_url.call_count, 3)
        mock_paths_less.assert_called_once_with(
            views="mock_views",
            model_list="mock_models",
            ignore_missing_views=True,
            list="",
            create="new/",
            detail="<str:pk>/",
        )
        self.assertEqual(result, "result")

    @patch("trim.urls.paths_less")
    @patch("trim.urls.trim_names")
    def test_paths_default_passes_ignore_flag(self, mock_trim_names, mock_paths_less):
        """Test paths_default passes ignore_missing_views flag."""
        # Setup
        mock_trim_names.get_url.return_value = ""
        mock_paths_less.return_value = "result"
        # Execute
        urls.paths_default("views", "models", ignore_missing_views=False, views=("list",))
        # Assert
        mock_paths_less.assert_called_once_with(
            views="views", model_list="models", ignore_missing_views=False, list=""
        )

    @patch("trim.urls.paths_named")
    def test_paths_less_converts_single_model(self, mock_paths_named):
        """Test paths_less converts single model to tuple."""
        # Setup
        mock_model = type("Product", (), {"__name__": "Product"})()
        mock_paths_named.return_value = ["path1", "path2"]
        # Execute
        result = urls.paths_less("views", mock_model, list="", create="new/")
        # Assert
        mock_paths_named.assert_called_once_with(
            "views",
            "Product",
            url_pattern_prefix="product/",
            ignore_missing_views=False,
            url_name_prefix="product-",
            list="",
            create="new/",
        )
        self.assertEqual(result, ["path1", "path2"])

    @patch("trim.urls.paths_named")
    def test_paths_less_handles_multiple_models(self, mock_paths_named):
        """Test paths_less calls paths_named for each model."""
        # Setup
        mock_model1 = type("Product", (), {"__name__": "Product"})()
        mock_model2 = type("Order", (), {"__name__": "Order"})()
        mock_paths_named.side_effect = [["path1"], ["path2"]]
        # Execute
        result = urls.paths_less("views", (mock_model1, mock_model2), list="")
        # Assert
        self.assertEqual(mock_paths_named.call_count, 2)
        self.assertEqual(result, ["path1", "path2"])

    @patch("trim.urls.paths_named")
    def test_paths_less_passes_ignore_flag(self, mock_paths_named):
        """Test paths_less passes ignore_missing_views flag."""
        # Setup
        mock_model = type("Product", (), {"__name__": "Product"})()
        mock_paths_named.return_value = []
        # Execute
        urls.paths_less("views", mock_model, ignore_missing_views=True)
        # Assert
        call_args = mock_paths_named.call_args[1]
        self.assertTrue(call_args["ignore_missing_views"])

    @patch("trim.urls.paths_dict")
    @patch("trim.urls.MAPPED_NAMES", {"list": "ListView"})
    def test_paths_named_converts_string_to_tuple(self, mock_paths_dict):
        """Test paths_named converts string pattern to tuple using MAPPED_NAMES."""
        # Setup
        mock_paths_dict.return_value = "result"
        # Execute
        result = urls.paths_named("views", list="")
        # Assert
        expected_patterns = {"ListView": ("list", "")}
        mock_paths_dict.assert_called_once_with(
            "views",
            expected_patterns,
            None,
            url_pattern_prefix=None,
            url_name_prefix=None,
            ignore_missing_views=False,
        )
        self.assertEqual(result, "result")

    @patch("trim.urls.paths_dict")
    def test_paths_named_preserves_tuple_patterns(self, mock_paths_dict):
        """Test paths_named preserves already-tuple patterns."""
        # Setup
        mock_paths_dict.return_value = "result"
        # Execute
        urls.paths_named("views", list=("ListView", ""))
        # Assert
        call_args = mock_paths_dict.call_args[0]
        patterns = call_args[1]
        self.assertEqual(patterns["ListView"], ("list", ""))

    @patch("trim.urls.paths_dict")
    def test_paths_named_passes_all_params(self, mock_paths_dict):
        """Test paths_named forwards all parameters to paths_dict."""
        # Setup
        mock_paths_dict.return_value = "result"
        # Execute
        urls.paths_named(
            "views",
            view_prefix="Product",
            ignore_missing_views=True,
            url_pattern_prefix="p/",
            url_name_prefix="prod-",
        )
        # Assert
        mock_paths_dict.assert_called_once_with(
            "views",
            {},
            "Product",
            url_pattern_prefix="p/",
            url_name_prefix="prod-",
            ignore_missing_views=True,
        )

    @patch("trim.urls.paths_dict")
    def test_paths_tuple_converts_tuples_to_dict(self, mock_paths_dict):
        """Test paths_tuple converts tuple patterns to dict format."""
        # Setup
        mock_paths_dict.return_value = "result"
        patterns = (("ListView", "list", ""), ("CreateView", "create", "new/"))
        # Execute
        result = urls.paths_tuple("views", patterns)
        # Assert
        expected_dict = {"ListView": ["list", ""], "CreateView": ["create", "new/"]}
        mock_paths_dict.assert_called_once_with("views", expected_dict)
        self.assertEqual(result, "result")

    @patch("trim.urls.paths_dict")
    def test_paths_tuple_forwards_kwargs(self, mock_paths_dict):
        """Test paths_tuple forwards additional kwargs to paths_dict."""
        # Setup
        mock_paths_dict.return_value = "result"
        patterns = (("ListView", "list", ""),)
        # Execute
        urls.paths_tuple("views", patterns, view_prefix="Product")
        # Assert
        call_kwargs = mock_paths_dict.call_args[1]
        self.assertEqual(call_kwargs["view_prefix"], "Product")
