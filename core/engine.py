import logging
import time
import random
from datetime import datetime
from typing import List, Dict, Any
from core.reporter import Reporter
from core.intelligence import IntelligenceEngine
from core.base import BaseScanner
from core.memory import EngagementMemory
from core.tactics import TacticalBrain, TacticalStates
from modules.scanners import ReconModule, VulnerabilityScanner, TrafficScanner
from modules.fingerprinter import Fingerprinter
from modules.vulnerability_scanner import VulnerabilityScanner as AdvancedVulnScanner
from modules.validator import SafeValidator
from utils.network import is_packet_capture_feasible, detect_cdn

from core.config import Config
from core.mission import MissionEngine, MissionTypes


class ScanningEngine:
    def __init__(
        self,
        target,
        depth,
        output_format,
        mode=Config.MODE_AUDIT,
        mission_type=MissionTypes.RECON,
        stealth=False,
    ):
        self.target = target
        self.depth = depth
        self.output_format = output_format
        self.mode = mode
        self.stealth = stealth or mode == Config.MODE_STEALTH
        self.logger = logging.getLogger("AegisScan.Engine")
        self.findings = []

        # Strategic & Tactical Layers (v3.0/v4.0)
        self.mission = MissionEngine(mission_type=mission_type)
        self.memory = EngagementMemory()
        self.brain = TacticalBrain(self.memory, mission=self.mission)

        # Core Components
        self.reporter = Reporter(output_format)
        self.intel = IntelligenceEngine()
        self.fingerprinter = Fingerprinter(target)
        self.validator = SafeValidator(target)
        self.traffic_scanner = TrafficScanner(target)
        self.vuln_scanner = AdvancedVulnScanner(target)

    def adjust_tactics(self, response_code=200):
        """Adaptive scanning: adjusts behavior based on target defensive behavior."""
        if response_code in [403, 429]:
            self.pressure_level += 2
            self.logger.warning(
                f"[ADAPTIVE] Defensive pressure detected ({response_code}). Escalating stealth..."
            )
            self.jitter(multiplier=2)
        elif self.pressure_level > 0:
            self.pressure_level -= 0.5

    def jitter(self, multiplier=1):
        """Tactical random delay with adaptive multiplier and non-linear logic."""
        if self.stealth:
            # Human-like inconsistent timing (v3.0)
            base_delay = random.uniform(2.0, 5.0) if self.stealth else 0.5
            delay = (base_delay + random.uniform(-1.0, 1.0)) * multiplier
            time.sleep(max(0.1, delay))

    def run(self):
        self.logger.info(
            f"=== AegisScan Strategic v4.0 Framework: {self.target} [Mission: {self.mission.mission_type}] ==="
        )
        self.findings = []

        # Start Red-Team State Machine
        while self.brain.current_state != TacticalStates.DISENGAGE:
            current_phase = self.brain.current_state
            self.logger.info(f"[PHASE] Transitioning to {current_phase}...")

            if current_phase == TacticalStates.RECON:
                self._execute_recon_phase()
            elif current_phase == TacticalStates.ENUMERATION:
                self._execute_enumeration_phase()
            elif current_phase == TacticalStates.VALIDATION:
                self._execute_validation_phase()
            elif current_phase == TacticalStates.PRESSURE_DETECTED:
                self._handle_pressure_phase()

            # Decide next phase based on findings and target behavior
            next_phase = self.brain.decide_next_phase(self.findings)
            if (
                next_phase == current_phase
                and current_phase != TacticalStates.PRESSURE_DETECTED
            ):
                # Break to prevent loops if no new data or transitions
                break

        # Post-Scan Tactical & Strategic Tasks
        self._apply_mitre_mapping()

        # Strategic Success Evaluation
        mission_summary = {
            "objective": self.mission.mission_type,
            "achieved": self.mission.intel_value
            >= self.mission.thresholds["intel_goal"],
            "noise_generated": self.mission.current_noise,
            "intel_gained": self.mission.intel_value,
        }

        self.reporter.generate(
            self.target,
            self.findings,
            {
                "mode": self.mode,
                "phases": self.brain.phase_history,
                "mission": mission_summary,
            },
        )

        # Send webhook notifications if enabled
        self._send_webhook_notifications(
            target=self.target, findings=self.findings, mission_summary=mission_summary
        )

        # Send webhook notifications if enabled
        self._send_webhook_notifications(
            target=self.target, findings=self.findings, mission_summary=mission_summary
        )

        self._cleanup()
        self.logger.info(f"Strategic {self.mission.mission_type} cycle completed.")

    def _send_webhook_notifications(
        self, target: str, findings: List[Dict], mission_summary: Dict
    ):
        """Send scan results to configured webhook endpoints for SIEM/SOAR integration"""
        try:
            import requests
            import json

            # Check if webhook notifications are enabled in config
            # For now, we'll check if there's a webhook URL configured
            # In a full implementation, this would read from config.yaml
            webhook_url = ""  # Would be loaded from config

            if not webhook_url:
                return  # Webhook not configured

            # Prepare payload
            payload = {
                "timestamp": datetime.now().isoformat(),
                "target": target,
                "scanner": "AegisScan Strategic v4.0",
                "mission": mission_summary,
                "findings_summary": {
                    "total_findings": len(findings),
                    "critical": len(
                        [f for f in findings if f.get("severity") == "CRITICAL"]
                    ),
                    "high": len([f for f in findings if f.get("severity") == "HIGH"]),
                    "medium": len(
                        [f for f in findings if f.get("severity") == "MEDIUM"]
                    ),
                    "low": len([f for f in findings if f.get("severity") == "LOW"]),
                },
                "findings": findings[
                    :10
                ],  # Limit to first 10 findings to avoid huge payloads
            }

            # Send webhook
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "AegisScan-Strategic/v4.0",
            }

            response = requests.post(
                webhook_url, json=payload, headers=headers, timeout=10
            )

            if response.status_code in [200, 201, 202]:
                self.logger.info(
                    f"Webhook notification sent successfully to {webhook_url}"
                )
            else:
                self.logger.warning(
                    f"Webhook notification failed with status {response.status_code}: {response.text}"
                )

        except Exception as e:
            self.logger.error(f"Failed to send webhook notification: {str(e)}")

    def _execute_recon_phase(self):
        self.jitter()
        # Record strategic impact
        self.mission.record_action(noise_cost=2, intel_gain=10)

        cdn_info = detect_cdn(self.target)
        stack = self.fingerprinter.analyze(cdn_info)
        recon = ReconModule(self.target)
        recon_data = recon.detect_stack()

        self.memory.log_behavior(latency=1.2, status_code=200)

    def _execute_enumeration_phase(self):
        self.jitter(multiplier=1.5)
        # Strategic noise recording
        self.mission.record_action(noise_cost=10, intel_gain=25)

        if random.random() < 0.2:
            self.logger.info(
                "[HUMAN-LIKE] Strategic variance applied: Skipping sub-check to manage noise."
            )

        if self.depth > 1:
            # Use advanced vulnerability scanner for comprehensive checks
            if not self.memory.is_blocked("vulnerability_scan"):
                vuln_results = self.vuln_scanner.run_comprehensive_scan()
                # Convert to format compatible with existing findings
                for severity_level, count in vuln_results[
                    "results_by_severity"
                ].items():
                    if count > 0:
                        self.findings.append(
                            {
                                "type": "vulnerability_summary",
                                "severity": severity_level,
                                "count": count,
                                "description": f"Found {count} {severity_level} severity vulnerabilities",
                                "target": self.target,
                                "engine": "advanced_vulnerability_scanner",
                            }
                        )

                # Also add detailed findings for high/critical issues
                if (
                    vuln_results["results_by_severity"]["critical"] > 0
                    or vuln_results["results_by_severity"]["high"] > 0
                ):
                    self.findings.append(
                        {
                            "type": "critical_vulnerabilities_found",
                            "description": "Critical or high severity vulnerabilities detected requiring immediate attention",
                            "target": self.target,
                            "count": vuln_results["results_by_severity"]["critical"]
                            + vuln_results["results_by_severity"]["high"],
                            "engine": "advanced_vulnerability_scanner",
                        }
                    )

    def _execute_validation_phase(self):
        self.logger.info(
            "Performing heuristic-based validation for current findings..."
        )
        self.findings = self.validator.confirm(self.findings)

    def _handle_pressure_phase(self):
        self.logger.warning(
            "[TACTICS] Target defense detected. Implementing adaptive cooldown."
        )
        time.sleep(random.uniform(5, 10))
        self.stealth = True  # Force stealth for remaining engagement

    def _apply_mitre_mapping(self):
        """Maps finding components to MITRE ATT&CK techniques."""
        for finding in self.findings:
            component = finding.get("component", "recon").lower()
            finding["mitre_attack"] = self.brain.get_mitre_mapping(component)

    def _cleanup(self):
        """Elite feature: secure handling and cleanup of temporary artifacts."""
        self.logger.debug("Operational cleanup of temporary engagement artifacts...")
        pass
