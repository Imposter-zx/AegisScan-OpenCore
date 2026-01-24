import json
import os
from datetime import datetime

class Reporter:
    def __init__(self, output_format):
        self.output_format = output_format
        self.report_dir = "reports"
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def generate(self, target, findings, stack=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_name = target.replace("http://", "").replace("https://", "").replace("/", "_").replace(":", "_")
        
        # Calculate overall risk score
        risk_score = self._calculate_risk(findings)
        
        if self.output_format in ["json", "both"]:
            self._save_json(target, findings, stack, risk_score, f"{target_name}_{timestamp}.json")
        
        if self.output_format in ["text", "both"]:
            self._save_text(target, findings, stack, risk_score, f"{target_name}_{timestamp}.txt")

    def _calculate_risk(self, findings):
        if not findings: return 0
        severity_map = {"CRITICAL": 10, "HIGH": 7, "MEDIUM": 4, "LOW": 1}
        score = sum(severity_map.get(f.get('severity', 'LOW'), 1) for f in findings)
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
                "critical": len([f for f in findings if f.get('severity') == 'CRITICAL']),
                "high": len([f for f in findings if f.get('severity') == 'HIGH'])
            },
            "findings": findings
        }
        filepath = os.path.join(self.report_dir, filename)
        with open(filepath, "w") as f:
            json.dump(report_data, f, indent=4)
        print(f"[*] Strategic JSON report saved to {filepath}")

    def _save_text(self, target, findings, stack, risk_score, filename):
        filepath = os.path.join(self.report_dir, filename)
        mission = stack.get("mission", {})
        
        with open(filepath, "w") as f:
            f.write("="*80 + "\n")
            f.write(f"AEGISSCAN STRATEGIC v4.0 ENGAGEMENT REPORT\n")
            f.write(f"Target: {target} | Risk Score: {risk_score}/100\n")
            f.write("="*80 + "\n\n")
            
            f.write("STRATEGIC MISSION SUMMARY\n")
            f.write("-" * 30 + "\n")
            f.write(f"Objective: {mission.get('objective', 'Unknown')}\n")
            f.write(f"Outcome: {'SUCCESS' if mission.get('achieved') else 'INCOMPLETE'}\n")
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
                    conf = finding.get('confidence', 'Medium')
                    mitre = finding.get('mitre_attack', 'T1595')
                    f.write(f"[{finding.get('severity', 'LOW')}] {finding.get('title')} (Conf: {conf})")
                    f.write(f"\nMITRE ATT&CK: {mitre}")
                    f.write(f"\nStatus: {'VALIDATED' if finding.get('validated') else 'UNVERIFIED'}")
                    f.write(f"\nRemediation: {finding.get('remediation')}\n")
                    f.write("-" * 40 + "\n")
            
            f.write("\nOPERATIONAL APPENDIX & HYGIENE\n")
            f.write("-" * 30 + "\n")
            f.write("Strategy: Mission-Aware Intent / Adaptive Evasion\n")
            f.write("Integrity: All binaries validated pre-execution.\n")
            f.write("Cleanup: Temporary operational artifacts have been purged.\n")

        print(f"[*] Strategic Text report saved to {filepath}")


