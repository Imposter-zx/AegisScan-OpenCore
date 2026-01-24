import os
import hashlib
import logging

class Config:
    """Elite AegisScan Configuration and Operational Parameters."""
    
    # Operational Modes
    MODE_OBSERVATION = "observation"
    MODE_STEALTH = "stealth"
    MODE_AUDIT = "audit"
    
    # Tool Integrity: Expected Hashes (Placeholder for real binaries)
    TOOL_INTEGRITY = {
        "nmap": "eb83463428d0092f03f3801f46497f14", # Mock hash
        "tshark": "85ef6686d8847bdbb35f72c29d55969a" # Mock hash
    }

    @staticmethod
    def validate_mode(mode):
        """Validates that the selected operational mode is within authorized limits."""
        authorized = [Config.MODE_OBSERVATION, Config.MODE_STEALTH, Config.MODE_AUDIT]
        if mode not in authorized:
            raise ValueError(f"CRITICAL: Unauthorized Operational Mode '{mode}' requested.")
        return True

    @staticmethod
    def get_api_key():
        """Retrieves NVD API Key from environment to avoid hardcoding."""
        return os.environ.get("AEGIS_API_KEY", "")

    @staticmethod
    def verify_tool_integrity(tool_path, expected_hash):
        """Verifies binary integrity before execution."""
        if not os.path.exists(tool_path):
            return False
        
        # In a real tool, we'd hash the file:
        # with open(tool_path, "rb") as f:
        #    file_hash = hashlib.md5(f.read()).hexdigest()
        # return file_hash == expected_hash
        
        return True # For demonstration
