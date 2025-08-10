"""Tests for trim.models.fields.base.defaults.

Covers:
- nil substitution to blank/null for True and False
- preserving existing params via setdefault
- reading nil from params when kw is absent
- honoring nil_sub flag (no substitution when False)
- removal of the 'nil' key from the result
"""

import unittest

from trim.models.fields.base import defaults


class DefaultsFunctionTestCase(unittest.TestCase):
    def test_nil_true_sets_blank_and_null_true(self):
        params = {}
        out = defaults((), params, nil=True)
        self.assertEqual(out.get("blank"), True)
        self.assertEqual(out.get("null"), True)
        self.assertNotIn("nil", out)

    def test_nil_false_sets_blank_and_null_false(self):
        params = {}
        out = defaults((), params, nil=False)
        self.assertEqual(out.get("blank"), False)
        self.assertEqual(out.get("null"), False)
        self.assertNotIn("nil", out)

    def test_preserves_existing_params_via_setdefault(self):
        params = {"blank": False}
        out = defaults((), params, nil=True)
        # existing blank remains, null is supplied by nil substitution
        self.assertEqual(out.get("blank"), False)
        self.assertEqual(out.get("null"), True)

    def test_nil_from_params_used_when_kw_absent(self):
        params = {"nil": False}
        out = defaults((), params)
        self.assertEqual(out.get("blank"), False)
        self.assertEqual(out.get("null"), False)
        self.assertNotIn("nil", out)

    def test_nil_sub_false_disables_substitution(self):
        params = {}
        out = defaults((), params, nil_sub=False, nil=True)
        # no blank/null added; 'nil' should not remain
        self.assertNotIn("blank", out)
        self.assertNotIn("null", out)
        self.assertNotIn("nil", out)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
