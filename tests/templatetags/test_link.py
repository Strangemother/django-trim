import unittest

# from django.test import RequestFactory
# from django.template import Context
from trim.templatetags import link as link_tags
from unittest.mock import patch


class TestLinkTemplateTags(unittest.TestCase):
    """Unit tests for link.py template tags and helpers."""

    # def setUp(self):
    #     self.factory = RequestFactory()
    #     self.context = Context({'request': self.factory.get('/')})

    def test_link_info(self):
        # Test the link_info simple tag
        with patch.object(link_tags, "link") as mock_link:
            link_tags.link_info("url", "text", foo="bar")
            mock_link.assert_called_once_with("url", "text", foo="bar")

    def test_link_info_url(self):
        # Test the link_info (url) simple tag
        with patch.object(link_tags, "link") as mock_link:
            url = "http://example.com"
            mock_link.return_value = {"url": url}
            res = link_tags.link_info("url", "text", foo="bar")
            mock_link.assert_called_once_with("url", "text", foo="bar")
            self.assertEqual(res, {"url": url})

    @patch("trim.templatetags.link.absolutify", return_value="http://example.com")
    @patch("trim.templatetags.link.gen_link")
    def test_abs_link(self, mock_gen_link, mock_absolutify):
        # Test abs_link inclusion tag
        # it calls gen_link and absolutify
        demo_url = "http://example.com"
        mock_gen_link.return_value = {"url": demo_url}
        context = {"request": "dummy_request"}
        res = link_tags.abs_link(context, "link", "text", foo="bar")

        mock_gen_link.assert_called_once_with("link", "text", foo="bar")
        mock_absolutify.assert_called_once_with(context["request"], demo_url)
        self.assertEqual(res["url"], demo_url)

    @patch("trim.templatetags.link.gen_link")
    def test_link(self, mock_gen_link):
        # Test link inclusion tag
        # it calls gen_link with correct parameters
        mock_gen_link.return_value = {
            "url": "http://example.com",
            "text": "text",
            "kwargs": {},
        }
        res = link_tags.link("link", "text", foo="bar")
        mock_gen_link.assert_called_once_with("link", "text", foo="bar")
        self.assertEqual(res["url"], "http://example.com")
        self.assertEqual(res["text"], "text")

    @patch("trim.templatetags.link.gen_link")
    def test_link_shadowdict(self, mock_gen_link):
        # if the link is a ShadowDict, it updates text and kwargs
        # mock_gen_link.return_value = {'url': 'http://example.com', 'text': 'text', 'kwargs': {'target': '_blank', 'rel': 'noreferrer noopener'}}
        link = link_tags.ShadowDict(
            {"url": "http://example.com", "text": "shadow owl", "kwargs": {}}
        )

        res = link_tags.link(link, "monkey", target="_self")
        self.assertEqual(res["text"], "monkey")
        # kwargs update the response.
        self.assertEqual(res["kwargs"]["target"], "_self")

    @patch("trim.templatetags.link.gen_link")
    def test_new_link(self, mock_gen_link):
        # Test new_link inclusion tag
        # it calls gen_link with target and rel set
        mock_gen_link.return_value = {
            "url": "http://example.com",
            "text": "text",
            "kwargs": {"target": "_blank", "rel": "noreferrer noopener"},
        }
        res = link_tags.new_link("link", "text")
        self.assertEqual(res["kwargs"]["target"], "_blank")
        self.assertEqual(res["kwargs"]["rel"], "noreferrer noopener")

    def test_script_link(self):
        # Test script_link inclusion tag
        # it returns a context with static_name, kwargs, and args
        res = link_tags.script_link("examples/js/my-js-file.js", "defer", "init")
        self.assertEqual(res["static_name"], "examples/js/my-js-file.js")
        self.assertEqual(res["kwargs"], {"type": "text/javascript"})
        self.assertEqual(res["args"], ("defer", "init"))

    def test_css_link(self):
        # Test css_link inclusion tag
        # it returns a context with static_name, kwargs, and args
        res = link_tags.css_link("examples/css/my-css-file.css", 'media="all"')
        self.assertEqual(res["static_name"], "examples/css/my-css-file.css")
        self.assertEqual(res["kwargs"], {"rel": "stylesheet", "type": "text/css"})
        self.assertEqual(res["args"], ('media="all"',))

    @patch("trim.templatetags.link.gen_link")
    def test_new_url_link(self, mock_gen_link):
        # Test new_url_link inclusion tag
        # it calls gen_link with url, target, and rel set
        mock_gen_link.return_value = {
            "url": "http://example.com",
            "text": "text",
            "kwargs": {"target": "_blank", "rel": "noreferrer noopener"},
        }
        res = link_tags.new_url_link("http://example.com", "text")
        self.assertEqual(res["kwargs"]["target"], "_blank")
        self.assertEqual(res["kwargs"]["rel"], "noreferrer noopener")

    @patch("trim.templatetags.link.gen_link")
    def test_url_link(self, mock_gen_link):
        # Test url_link inclusion tag
        # it calls gen_link with url
        mock_gen_link.return_value = {"url": "http://example.com"}
        res = link_tags.url_link("http://example.com")
        mock_gen_link.assert_called_once_with(
            "http://example.com", url="http://example.com"
        )
        self.assertEqual(res["url"], "http://example.com")

    def test_shadowdict(self):
        # Test ShadowDict class
        d = link_tags.ShadowDict({"a": 1})
        self.assertEqual(d["a"], 1)

    @patch("trim.templatetags.link.reverse")
    def test_gen_link(self, mock_reverse):
        # Test gen_link helper function
        # it calls reverse and returns a ShadowDict with url, text, kwargs
        mock_reverse.return_value = "http://example.com"
        res = link_tags.gen_link("view_name", "text", foo="bar")
        self.assertIsInstance(res, link_tags.ShadowDict)
        self.assertEqual(res["url"], "http://example.com")
        self.assertEqual(res["text"], "text")
        self.assertEqual(res["kwargs"], {"foo": "bar"})
