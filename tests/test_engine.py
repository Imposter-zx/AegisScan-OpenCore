import unittest
import sys
import os
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestScanningEngine(unittest.TestCase):
    """Test cases for the ScanningEngine class"""

    @patch("core.engine.ReconModule")
    @patch("core.engine.Fingerprinter")
    @patch("core.engine.detect_cdn")
    def test_recon_phase_execution(
        self, mock_detect_cdn, mock_fingerprinter, mock_recon
    ):
        """Test that recon phase executes without error"""
        from core.engine import ScanningEngine

        mock_detect_cdn.return_value = {"provider": "Cloudflare"}
        mock_fingerprinter.return_value.analyze.return_value = {"server": "nginx"}

        engine = ScanningEngine(
            target="test.example.com",
            depth=1,
            output_format="json",
            mode="audit",
            mission_type="RECON",
            stealth=False,
        )

        engine._execute_recon_phase()
        self.assertIsNotNone(engine.findings)
        self.assertIsInstance(engine.findings, list)

    def test_jitter_with_stealth(self):
        """Test that jitter runs without error in stealth mode"""
        from core.engine import ScanningEngine

        engine = ScanningEngine(
            target="test.example.com",
            depth=1,
            output_format="json",
            mode="stealth",
            stealth=True,
        )

        engine.jitter(multiplier=1)
        self.assertTrue(engine.stealth)

    def test_engine_initialization(self):
        """Test engine initialization with various parameters"""
        from core.engine import ScanningEngine

        engine = ScanningEngine(
            target="test.example.com",
            depth=2,
            output_format="both",
            mode="audit",
            mission_type="VALIDATION",
            stealth=False,
        )

        self.assertEqual(engine.target, "test.example.com")
        self.assertEqual(engine.depth, 2)
        self.assertEqual(engine.mode, "audit")


class TestReporter(unittest.TestCase):
    """Test cases for the Reporter class"""

    def test_json_report_format(self):
        """Test that JSON report generation works"""
        from core.reporter import Reporter
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reporter = Reporter("json")
            reporter.report_dir = tmpdir
            reporter.generate(
                target="test.example.com",
                findings=[
                    {
                        "severity": "HIGH",
                        "title": "Test finding",
                        "type": "vulnerability_summary",
                        "count": 1,
                    }
                ],
                stack={
                    "mode": "audit",
                    "phases": ["RECON"],
                    "mission": {"objective": "RECON"},
                },
            )
            self.assertIsNotNone(reporter)

    def test_text_report_format(self):
        """Test that text report generation works"""
        from core.reporter import Reporter
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reporter = Reporter("text")
            reporter.report_dir = tmpdir
            reporter.generate(
                target="test.example.com",
                findings=[],
                stack={"mode": "audit", "phases": [], "mission": {}},
            )
            self.assertIsNotNone(reporter)


if __name__ == "__main__":
    unittest.main()
