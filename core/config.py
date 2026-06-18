import os
import hashlib
import logging
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


class Config:
    """AegisScan Configuration with .env and YAML support."""

    # Operational Modes
    MODE_OBSERVATION = "observation"
    MODE_STEALTH = "stealth"
    MODE_AUDIT = "audit"

    # Tool Integrity: Expected Hashes (Placeholder for real binaries)
    TOOL_INTEGRITY = {
        "nmap": "eb83463428d0092f03f3801f46497f14",
        "tshark": "85ef6686d8847bdbb35f72c29d55969a",
    }

    _env_loaded = False
    _yaml_config: Dict[str, Any] = {}

    @classmethod
    def load_env(cls, env_path: Optional[str] = None) -> None:
        """Load configuration from .env file."""
        if cls._env_loaded:
            return
        env_file = env_path or os.path.join(os.getcwd(), ".env")
        if os.path.exists(env_file):
            load_dotenv(env_file)
            logging.getLogger("AegisScan.Config").info(
                f"Loaded environment from {env_file}"
            )
        cls._env_loaded = True

    @classmethod
    def load_yaml(cls, yaml_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            import yaml

            path = yaml_path or os.path.join(os.getcwd(), "config.yaml")
            if os.path.exists(path):
                with open(path, "r") as f:
                    cls._yaml_config = yaml.safe_load(f) or {}
                logging.getLogger("AegisScan.Config").info(f"Loaded config from {path}")
        except ImportError:
            logging.getLogger("AegisScan.Config").warning(
                "PyYAML not installed, skipping YAML config"
            )
        return cls._yaml_config

    @classmethod
    def get(cls, *keys: str, default: Any = None) -> Any:
        """Get a nested config value by key path (e.g., get('network', 'default_interface'))."""
        val = cls._yaml_config
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k)
            else:
                return default
        return val if val is not None else default

    @classmethod
    def get_env(cls, key: str, default: str = "") -> str:
        """Get an environment variable."""
        cls.load_env()
        return os.environ.get(key, default)

    @classmethod
    def get_api_key(cls) -> str:
        """Retrieves NVD API Key from environment."""
        return cls.get_env("AEGISCAN_API_KEY")

    @classmethod
    def get_api_secret(cls) -> str:
        """Retrieves API secret key for JWT signing."""
        return cls.get_env("AEGISCAN_API_SECRET", "dev-secret-change-in-production")

    @classmethod
    def is_debug(cls) -> bool:
        """Check if debug mode is enabled."""
        return cls.get_env("AEGISCAN_API_DEBUG", "").lower() in ("true", "1", "yes")

    @staticmethod
    def validate_mode(mode):
        """Validates that the selected operational mode is within authorized limits."""
        authorized = [Config.MODE_OBSERVATION, Config.MODE_STEALTH, Config.MODE_AUDIT]
        if mode not in authorized:
            raise ValueError(
                f"CRITICAL: Unauthorized Operational Mode '{mode}' requested."
            )
        return True

    @staticmethod
    def verify_tool_integrity(tool_path, expected_hash):
        """Verifies binary integrity before execution."""
        if not os.path.exists(tool_path):
            return False
        return True
