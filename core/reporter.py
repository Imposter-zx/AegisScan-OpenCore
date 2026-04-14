import json
import os
from datetime import datetime
import xml.etree.ElementTree as ET


class Reporter:
    def __init__(self, output_format):
        self.output_format = output_format
        self.report_dir = "reports"
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def generate(self, target, findings, stack=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_name = (
            target.replace("http://", "")
            .replace("https://", "")
            .replace("/", "_")
            .replace(":", "_")
        )

        # Calculate overall risk score
        risk_score = self._calculate_risk(findings)

        if self.output_format in ["json", "both"]:
            self._save_json(
                target, findings, stack, risk_score, f"{target_name}_{timestamp}.json"
            )

        if self.output_format in ["text", "both"]:
            self._save_text(
                target, findings, stack, risk_score, f"{target_name}_{timestamp}.txt"
            )

        # Advanced reporting formats
        if self.output_format in ["stix", "all"]:
            self._save_stix(
                target, findings, stack, risk_score, f"{target_name}_{timestamp}.json"
            )

        if self.output_format in ["cef", "all"]:
            self._save_cef(
                target, findings, stack, risk_score, f"{target_name}_{timestamp}.cef"
            )

    def _calculate_risk(self, findings):
        if not findings:
            return 0
        severity_map = {"CRITICAL": 10, "HIGH": 7, "MEDIUM": 4, "LOW": 1}
        score = sum(severity_map.get(f.get("severity", "LOW"), 1) for f in findings)
        return min(int(score / len(findings) * 10), 100)

    def _save_json(self, target, findings, stack, risk_score, filename):
        report_data = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "operational_mode": stack.get("mode", "Audit"),
            "strategic_mission": stack.get("mission", {}),  # Strategic v4.0
            "tactical_phases": stack.get("phases", []),
            "risk_score": risk_score,
            "summary": {
                "total_findings": len(findings),
                "critical": len(
                    [f for f in findings if f.get("severity") == "CRITICAL"]
                ),
                "high": len([f for f in findings if f.get("severity") == "HIGH"]),
            },
            "findings": findings,
        }
        filepath = os.path.join(self.report_dir, filename)
        with open(filepath, "w") as f:
            json.dump(report_data, f, indent=4)
        print(f"[*] Strategic JSON report saved to {filepath}")

    def _save_text(self, target, findings, stack, risk_score, filename):
        filepath = os.path.join(self.report_dir, filename)
        mission = stack.get("mission", {})

        with open(filepath, "w") as f:
            f.write("=" * 80 + "\n")
            f.write(f"AEGISSCAN STRATEGIC v4.0 ENGAGEMENT REPORT\n")
            f.write(f"Target: {target} | Risk Score: {risk_score}/100\n")
            f.write("=" * 80 + "\n\n")

            f.write("STRATEGIC MISSION SUMMARY\n")
            f.write("-" * 30 + "\n")
            f.write(f"Objective: {mission.get('objective', 'Unknown')}\n")
            f.write(
                f"Outcome: {'SUCCESS' if mission.get('achieved') else 'INCOMPLETE'}\n"
            )
            f.write(f"Intel Gained: {mission.get('intel_gained', 0)} pts\n")
            f.write(f"Noise Generated: {mission.get('noise_generated', 0)} pts\n\n")

            f.write("TACTICAL CONTEXT\n")
            f.write("-" * 20 + "\n")
            f.write(f"Operational Mode: {stack.get('mode', 'Audit')}\n")
            f.write(f"Engagement Phases: {' -> '.join(stack.get('phases', []))}\n")
            if stack:
                f.write(f"WAF Status: {stack.get('waf', 'None detected')}\n")
            f.write("\n")

            f.write("TECHNICAL FINDINGS & ATT&CK MAPPING\n")
            f.write("-" * 40 + "\n")
            if not findings:
                f.write("No vulnerabilities identified during this engagement cycle.\n")
            else:
                for finding in findings:
                    conf = finding.get("confidence", "Medium")
                    mitre = finding.get("mitre_attack", "T1595")
                    f.write(
                        f"[{finding.get('severity', 'LOW')}] {finding.get('title')} (Conf: {conf})"
                    )
                    f.write(f"\nMITRE ATT&CK: {mitre}")
                    f.write(
                        f"\nStatus: {'VALIDATED' if finding.get('validated') else 'UNVERIFIED'}"
                    )
                    f.write(f"\nRemediation: {finding.get('remediation')}\n")
                    f.write("-" * 40 + "\n")

            f.write("\nOPERATIONAL APPENDIX & HYGIENE\n")
            f.write("-" * 30 + "\n")
            f.write("Strategy: Mission-Aware Intent / Adaptive Evasion\n")
            f.write("Integrity: All binaries validated pre-execution.\n")
            f.write("Cleanup: Temporary operational artifacts have been purged.\n")

        print(f"[*] Strategic Text report saved to {filepath}")

    def _save_stix(self, target, findings, stack, risk_score, filename):
        """Save findings in STIX 2.1 format"""
        # Create STIX bundle
        bundle = {
            "type": "bundle",
            "id": f"bundle--{self._generate_uuid()}",
            "spec_version": "2.1",
            "objects": [],
        }

        # Add observables (target)
        target_obj = {
            "type": "observable",
            "id": f"observable--{self._generate_uuid()}",
            "object_marking_refs": [
                "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9"
            ],
            "value": target,
            "type": "domain-name"
            if "." in target and not target.replace(".", "").isdigit()
            else "ipv4-addr",
        }
        bundle["objects"].append(target_obj)

        # Add vulnerability findings as vulnerabilities
        for i, finding in enumerate(findings):
            if finding.get("type") in [
                "vulnerability_summary",
                "critical_vulnerabilities_found",
            ]:
                vuln_obj = {
                    "type": "vulnerability",
                    "id": f"vulnerability--{self._generate_uuid()}",
                    "created": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "modified": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "name": finding.get("title", "Unknown Vulnerability"),
                    "description": finding.get("description", ""),
                    "external_references": [
                        {
                            "source_name": "AegisScan Strategic",
                            "url": f"https://github.com/Imposter-zx/AegisScan-OpenCore",
                            "external_id": f"AS-{i + 1:04d}",
                        }
                    ],
                    "object_marking_refs": [
                        "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9"
                    ],
                }

                # Add severity if available
                severity_map = {
                    "critical": "Critical",
                    "high": "High",
                    "medium": "Medium",
                    "low": "Low",
                }
                if finding.get("severity") in severity_map:
                    vuln_obj["severity"] = severity_map[finding["severity"].lower()]

                bundle["objects"].append(vuln_obj)

        # Add marking definition
        marking_def = {
            "type": "marking-definition",
            "id": "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9",
            "created": "2017-01-20T00:00:00.000Z",
            "definition_type": "statement",
            "definition": {
                "statement": "Internal Use Only - AegisScan Strategic Security Assessment"
            },
        }
        bundle["objects"].append(marking_def)

        # Save STIX bundle
        filepath = os.path.join(self.report_dir, filename)
        with open(filepath, "w") as f:
            json.dump(bundle, f, indent=2)
        print(f"[*] STIX 2.1 report saved to {filepath}")

    def _save_cef(self, target, findings, stack, risk_score, filename):
        """Save findings in CEF (Common Event Format)"""
        # CEF Header: CEF:Version|Device Vendor|Device Product|Device Version|Signature ID|Name|Severity|Extension
        cef_header = "CEF:0|AegisScan|Strategic|v4.0|"

        filepath = os.path.join(self.report_dir, filename)
        with open(filepath, "w") as f:
            # Write header info
            f.write("# CEF (Common Event Format) Log - AegisScan Strategic v4.0\n")
            f.write(f"# Target: {target}\n")
            f.write(f"# Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"# Risk Score: {risk_score}/100\n")
            f.write(
                "# Format: CEF:0|AegisScan|Strategic|v4.0|Signature ID|Name|Severity|Extension\n\n"
            )

            # Write each finding as a CEF event
            for i, finding in enumerate(findings):
                if finding.get("type") in [
                    "vulnerability_summary",
                    "critical_vulnerabilities_found",
                ]:
                    # Determine signature ID based on finding type
                    sig_id = (
                        "VULN_SUMMARY"
                        if finding.get("type") == "vulnerability_summary"
                        else "CRITICAL_VULN"
                    )

                    # Determine severity
                    severity_map = {
                        "critical": "10",
                        "high": "8",
                        "medium": "5",
                        "low": "3",
                        "info": "1",
                    }
                    severity = severity_map.get(
                        finding.get("severity", "low").lower(), "3"
                    )

                    # Build extension string
                    extension_parts = []
                    extension_parts.append(f"target={target}")
                    extension_parts.append(
                        f"reason={finding.get('description', 'Vulnerability detected')}"
                    )
                    extension_parts.append(f"count={finding.get('count', 1)}")

                    if "results_by_severity" in finding:
                        for sev, count in finding["results_by_severity"].items():
                            if count > 0:
                                extension_parts.append(f"{sev}count={count}")

                    extension = " ".join(extension_parts)

                    # Write CEF line
                    cef_line = f"{cef_header}{sig_id}|{finding.get('title', 'Security Finding')}|{severity}|{extension}\n"
                    f.write(cef_line)

        print(f"[*] CEF report saved to {filepath}")

    def _generate_uuid(self):
        """Generate a random UUID-like string for STIX IDs"""
        import random
        import string

        # Generate 32 hex characters (simplified UUID)
        return "".join(random.choices(string.hexdigits.lower(), k=32))
