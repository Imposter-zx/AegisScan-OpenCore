import logging

class EngagementMemory:
    """Session-based memory for tracking tactical successes and failures."""
    
    def __init__(self):
        self.logger = logging.getLogger("AegisScan.Memory")
        self.blocked_techniques = set()
        self.successful_evasions = set()
        self.waf_signatures = set()
        self.target_behavior_history = [] # Tracks latency, response codes

    def record_block(self, technique_id, details=""):
        self.logger.warning(f"[MEMORY] Technique {technique_id} was blocked/slowed. Recording for avoidance.")
        self.blocked_techniques.add(technique_id)

    def record_success(self, evasion_id):
        self.logger.info(f"[MEMORY] Evasion pattern {evasion_id} was successful. Biasing future decisions.")
        self.successful_evasions.add(evasion_id)

    def is_blocked(self, technique_id):
        return technique_id in self.blocked_techniques

    def log_behavior(self, latency, status_code):
        self.target_behavior_history.append({"latency": latency, "status_code": status_code})
        if len(self.target_behavior_history) > 10:
            self.target_behavior_history.pop(0)

    def get_session_pressure(self):
        """Analyzes history to determine current defensive pressure."""
        if not self.target_behavior_history:
            return 0
        
        errors = [h['status_code'] for h in self.target_behavior_history if h['status_code'] in [403, 429]]
        return (len(errors) / len(self.target_behavior_history)) * 10
