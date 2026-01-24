import logging

class TacticalStates:
    RECON = "RECON"
    ENUMERATION = "ENUMERATION"
    VALIDATION = "VALIDATION"
    PRESSURE_DETECTED = "PRESSURE_DETECTED"
    DISENGAGE = "DISENGAGE"

class TacticalBrain:
    """The tactical intelligence layer that decides the next attack phase."""
    
    def __init__(self, memory, mission=None):
        self.memory = memory
        self.mission = mission
        self.logger = logging.getLogger("AegisScan.Tactics")
        self.current_state = TacticalStates.RECON
        self.phase_history = []

    def decide_next_phase(self, last_results=None):
        """Strategic decision logic to transition between red-team phases."""
        pressure = self.memory.get_session_pressure()
        
        # 1. Strategic Halt Conditions
        if self.mission and self.mission.should_disengage():
            self.logger.critical("[STRATEGIC] Mission Halt reached. Disengaging.")
            self.current_state = TacticalStates.DISENGAGE
            return self.current_state

        if pressure > 7:
            self.logger.critical("[TACTICS] High defensive pressure detected. Force transitioning to DISENGAGE.")
            self.current_state = TacticalStates.DISENGAGE
            return self.current_state

        # 2. Mission-Aware Transitions
        if self.mission:
            health = self.mission.evaluate_gain_vs_exposure()
            if health == "CAUTION":
                self.logger.warning("[STRATEGIC] Strategic caution applied. Avoiding aggressive phases.")
                if self.current_state != TacticalStates.RECON:
                    self.current_state = TacticalStates.PRESSURE_DETECTED
                    return self.current_state

        if pressure > 4:
            self.logger.warning("[TACTICS] Moderate pressure. Moving to PRESSURE_DETECTED protocols.")
            self.current_state = TacticalStates.PRESSURE_DETECTED
            return self.current_state

        # 3. Tactical Progression
        if self.current_state == TacticalStates.RECON:
            if last_results and len(last_results) > 0:
                self.current_state = TacticalStates.ENUMERATION
        elif self.current_state == TacticalStates.ENUMERATION:
            if last_results and any(f.get('severity') in ['HIGH', 'CRITICAL'] for f in last_results):
                # Only proceed to validation if intel gain justifies the noise (Mission Logic)
                if self.mission and self.mission.intel_value > 20: 
                    self.current_state = TacticalStates.VALIDATION
                else:
                    self.logger.info("[STRATEGIC] Insufficient intel value to justify active validation. Staying in Enumeration.")
        
        self.phase_history.append(self.current_state)
        return self.current_state


    def get_mitre_mapping(self, technique_name):
        """Maps framework actions to MITRE ATT&CK techniques."""
        mapping = {
            "nmap": "T1595.001 (Active Scanning)",
            "tshark": "T1040 (Network Sniffing)",
            "httpx": "T1592 (Gather Victim Host Information)",
            "cve_match": "T1595.002 (Vulnerability Scanning)"
        }
        return mapping.get(technique_name, "T1595 (Active Scanning)")
