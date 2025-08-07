"""
Unit tests for src/trim/models/live.py
"""
import unittest
from trim.models.live import MagicModelApp, MagicModelModel
from trim.models import live
from unittest.mock import patch

class TestMagicModelApp(unittest.TestCase):
    """Test the MagicModelApp class."""
    def setUp(self):
        self.magic_app = live

    @patch('trim.models.live.apps.get_model')
    def test_getattr_returns_magic_model_model(self, mock_get_model):
        # Setup: Access an app name attribute
        # Expected: Should return a MagicModelModel instance
        # Result: Check type
        model = live.baskets
        self.assertIsInstance(model, MagicModelModel)
        self.assertEqual(model.appname, 'baskets')    

        model = live.bilko.Florp
        mock_get_model.assert_called_once_with('bilko', 'Florp')
