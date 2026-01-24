import logging

class MissionTypes:
    RECON = "RECON"                     # Goal: Intelligence Gain. Profile: Stealthy.
    VALIDATION = "VALIDATION"           # Goal: Confirm Exposure. Profile: Accurate.
    EMULATION = "EMULATION"             # Goal: Defensive Training. Profile: Noisy/Realistic.

class MissionEngine:
    """The strategic mission layer for intent-aware operations."""
    
    def __init__(self, mission_type=MissionTypes.RECON, noise_budget=50):
        self.mission_type = mission_type
        self.noise_budget = noise_budget # Max allowed "noise" before disengagement
        self.current_noise = 0
        self.risk_level = 0
        self.intel_value = 0
        self.logger = logging.getLogger("AegisScan.Mission")
        
        # Strategic thresholds based on mission type
        self.thresholds = self._get_thresholds()

    def _get_thresholds(self):
        if self.mission_type == MissionTypes.RECON:
            return {"noise_limit": 30, "intel_goal": 50, "disengage_on_detection": True}
        elif self.mission_type == MissionTypes.VALIDATION:
            return {"noise_limit": 70, "intel_goal": 80, "disengage_on_detection": False}
        else: # EMULATION
            return {"noise_limit": 100, "intel_goal": 100, "disengage_on_detection": False}

    def record_action(self, noise_cost=5, intel_gain=10):
        """Records an action and its strategic impact."""
        self.current_noise += noise_cost
        self.intel_value += intel_gain
        self.logger.info(f"[MISSION] Budget Update: Noise {self.current_noise}/{self.noise_budget} | Intel {self.intel_value}/Goal")

    def should_disengage(self):
        """Strategic stop condition check."""
        if self.current_noise >= self.noise_budget:
            self.logger.critical("[STRATEGIC] Noise budget EXCEEDED. Initiating tactical disengagement.")
            return True
        return False

    def evaluate_gain_vs_exposure(self):
        """Analyzes mission health like a senior operator."""
        if self.intel_value > 0 and self.current_noise > 0:
            ratio = self.intel_value / self.current_noise
            if ratio < 0.5 and self.mission_type == MissionTypes.RECON:
                self.logger.warning("[STRATEGIC] High Exposure/Low Gain detected. Recommending restraint.")
                return "CAUTION"
        return "STABLE"
