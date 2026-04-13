import unittest
import sys
import os

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for the Config class"""

    def test_validate_mode_valid(self):
        """Test that valid modes pass validation"""
        self.assertTrue(Config.validate_config(Config.MODE_AUDIT))
        self.assertTrue(Config.validate_config(Config.MODE_STEALTH))
        self.assertTrue(Config.validate_config(Config.MODE_OBSERVATION))

    def test_validate_mode_invalid(self):
        """Test that invalid modes raise ValueError"""
        with self.assertRaises(ValueError):
            Config.validate_mode("invalid_mode")

    def test_get_api_key(self):
        """Test API key retrieval"""
        # Should return empty string when no env var is set
        self.assertEqual(Config.get_api_key(), "")


if __name__ == "__main__":
    unittest.main()
