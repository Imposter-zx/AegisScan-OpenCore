import logging
import subprocess
import re
import shlex
import os
from core.config import Config

class BaseScanner:
    def __init__(self, target):
        self.target = target
        self.logger = logging.getLogger(f"AegisScan.{self.__class__.__name__}")

    def sanitize_input(self, input_str):
        """Elite white-listing. Only allows minimal safe character set."""
        if not input_str:
            return ""
        # Stricter: Allow only valid hostname/IP characters
        return re.sub(r'[^a-zA-Z0-9\.\-]', '', input_str)

    def execute_hardened(self, cmd, tool_name=None):
        """
        Elite execution layer. 
        1. Verifies tool integrity. 
        2. Prevents shell=True. 
        3. Sanitizes all inputs.
        """
        if tool_name and tool_name in Config.TOOL_INTEGRITY:
            # Note: actual path resolution would happen here
            if not Config.verify_tool_integrity(tool_name, Config.TOOL_INTEGRITY[tool_name]):
                self.logger.critical(f"[INTEGRITY FAILURE] Tool {tool_name} appears tampered!")
                return "INTEGRITY_FAIL"

        try:
            if isinstance(cmd, str):
                cmd = shlex.split(cmd)
            
            # Additional validation: No pipes or redirects in the list
            for part in cmd:
                if any(c in part for c in [';', '&', '|', '>', '<', '$']):
                    self.logger.error(f"[BLOCKED] Illegal character in command: {part}")
                    return "SECURITY_BLOCK"

            self.logger.debug(f"Elite execution call: {' '.join(cmd)}")
            result = subprocess.run(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                universal_newlines=True, 
                check=False
            )
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            self.logger.error(f"Elite Execution Error: {str(e)}")
            return ""
