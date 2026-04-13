import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestScanningEngine(unittest.TestCase):
    """Test cases for the ScanningEngine class"""

    @patch("core.engine.ScanningEngine.__init__", return_value=None)
    def test_engine_initialization(self, mock_init):
        """Test that we can initialize the engine (mocked)"""
        from core.engine import ScanningEngine

        # Create a mock instance
        engine = ScanningEngine.__new__(ScanningEngine)
        mock_init(engine, "test.target", 1, "text")

        # Verify initialization was called with correct args
        mock_init.assert_called_once_with(
            "test.target", 1, "text", mode="audit", mission_type="RECON", stealth=False
        )


if __name__ == "__main__":
    unittest.main()
