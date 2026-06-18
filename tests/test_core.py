import unittest
import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.config import Config
from core.mission import MissionEngine, MissionTypes
from core.tactics import TacticalBrain, TacticalStates
from core.memory import EngagementMemory
from core.base import BaseScanner


class TestConfig(unittest.TestCase):
    """Test cases for the Config class"""

    def test_validate_mode_valid(self):
        self.assertTrue(Config.validate_mode(Config.MODE_AUDIT))
        self.assertTrue(Config.validate_mode(Config.MODE_STEALTH))
        self.assertTrue(Config.validate_mode(Config.MODE_OBSERVATION))

    def test_validate_mode_invalid(self):
        with self.assertRaises(ValueError):
            Config.validate_mode("invalid_mode")
        with self.assertRaises(ValueError):
            Config.validate_mode("")

    def test_get_api_key(self):
        self.assertEqual(Config.get_api_key(), "")

    def test_get_env(self):
        val = Config.get_env("AEGISCAN_API_SECRET", "default_val")
        self.assertIsInstance(val, str)

    def test_is_debug_default(self):
        self.assertFalse(Config.is_debug())

    def test_tool_integrity_keys(self):
        self.assertIn("nmap", Config.TOOL_INTEGRITY)
        self.assertIn("tshark", Config.TOOL_INTEGRITY)

    def test_verify_tool_integrity_nonexistent(self):
        self.assertFalse(Config.verify_tool_integrity("/nonexistent/path", "abc"))


class TestMissionEngine(unittest.TestCase):
    """Test cases for the MissionEngine class"""

    def setUp(self):
        self.mission = MissionEngine(mission_type=MissionTypes.RECON)

    def test_initial_state(self):
        self.assertEqual(self.mission.mission_type, MissionTypes.RECON)
        self.assertEqual(self.mission.current_noise, 0)
        self.assertEqual(self.mission.intel_value, 0)

    def test_record_action(self):
        self.mission.record_action(noise_cost=10, intel_gain=25)
        self.assertEqual(self.mission.current_noise, 10)
        self.assertEqual(self.mission.intel_value, 25)

    def test_record_action_multiple(self):
        self.mission.record_action(noise_cost=5, intel_gain=10)
        self.mission.record_action(noise_cost=3, intel_gain=5)
        self.assertEqual(self.mission.current_noise, 8)
        self.assertEqual(self.mission.intel_value, 15)

    def test_thresholds_exist(self):
        self.assertIn("noise_limit", self.mission.thresholds)
        self.assertIn("intel_goal", self.mission.thresholds)


class TestTacticalBrain(unittest.TestCase):
    """Test cases for the TacticalBrain class"""

    def setUp(self):
        self.memory = EngagementMemory()
        self.mission = MissionEngine(mission_type=MissionTypes.RECON)
        self.brain = TacticalBrain(self.memory, mission=self.mission)

    def test_initial_state(self):
        self.assertIsNotNone(self.brain.current_state)

    def test_decide_next_phase(self):
        next_phase = self.brain.decide_next_phase([])
        self.assertIsNotNone(next_phase)

    def test_get_mitre_mapping(self):
        mapping = self.brain.get_mitre_mapping("recon")
        self.assertIsInstance(mapping, str)

    def test_phase_history(self):
        self.assertIsInstance(self.brain.phase_history, list)


class TestBaseScanner(unittest.TestCase):
    """Test cases for the BaseScanner class"""

    def setUp(self):
        self.scanner = BaseScanner("test.target.com")

    def test_target_set(self):
        self.assertEqual(self.scanner.target, "test.target.com")

    def test_sanitize_input(self):
        sanitized = self.scanner.sanitize_input("example.com; rm -rf /")
        self.assertNotIn(";", sanitized)


class TestEngagementMemory(unittest.TestCase):
    """Test cases for the EngagementMemory class"""

    def setUp(self):
        self.memory = EngagementMemory()

    def test_log_behavior(self):
        self.memory.log_behavior(latency=1.2, status_code=200)
        self.assertGreater(len(self.memory.target_behavior_history), 0)

    def test_is_blocked_initially(self):
        self.assertFalse(self.memory.is_blocked("vulnerability_scan"))

    def test_record_block(self):
        self.memory.record_block("vuln_scan")
        self.assertTrue(self.memory.is_blocked("vuln_scan"))

    def test_get_session_pressure_empty(self):
        pressure = self.memory.get_session_pressure()
        self.assertEqual(pressure, 0)

    def test_get_session_pressure_with_errors(self):
        self.memory.log_behavior(latency=1.0, status_code=403)
        self.memory.log_behavior(latency=0.5, status_code=200)
        pressure = self.memory.get_session_pressure()
        self.assertGreater(pressure, 0)
        self.assertIsInstance(pressure, (int, float))

    def test_record_success(self):
        self.memory.record_success("evasion_01")
        self.assertIn("evasion_01", self.memory.successful_evasions)


if __name__ == "__main__":
    unittest.main()
