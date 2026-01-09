"""
Test trim.models.fields.base module.
"""

import pytest
from trim.models.fields.base import defaults, blank_null


class TestBlankNull:
    """Test blank_null helper function."""

    def test_defaults(self):
        assert blank_null() == {"blank": True, "null": True}

    def test_custom_values(self):
        assert blank_null(False, False) == {"blank": False, "null": False}

    def test_mixed_values(self):
        assert blank_null(True, False) == {"blank": True, "null": False}


class TestDefaults:
    """Test defaults helper function."""

    def test_basic_merge(self):
        result = defaults([], {}, foo="bar")
        assert result == {"foo": "bar"}

    def test_preserve_existing(self):
        result = defaults([], {"foo": "baz"}, foo="bar")
        assert result == {"foo": "baz"}

    def test_nil_substitution_true(self):
        result = defaults([], {}, nil=True, other="val")
        assert result == {"blank": True, "null": True, "other": "val"}
        assert "nil" not in result

    def test_nil_substitution_false(self):
        result = defaults([], {}, nil=False, other="val")
        assert result == {"blank": False, "null": False, "other": "val"}
        assert "nil" not in result

    def test_nil_in_params(self):
        result = defaults([], {"nil": True}, other="val")
        assert result == {"blank": True, "null": True, "other": "val"}

    def test_nil_disabled(self):
        result = defaults([], {}, nil_sub=False, nil=True, other="val")
        assert result == {"other": "val"}
        assert "nil" not in result

    def test_custom_nil_key(self):
        result = defaults([], {}, nil_key="custom", custom=True)
        assert result == {"blank": True, "null": True}
        assert "custom" not in result

    def test_nil_non_bool_ignored(self):
        result = defaults([], {}, nil="string", other="val")
        assert result == {"other": "val"}
        assert "nil" not in result

    def test_multiple_params(self):
        result = defaults([], {}, foo="a", bar="b", baz="c")
        assert result == {"foo": "a", "bar": "b", "baz": "c"}
