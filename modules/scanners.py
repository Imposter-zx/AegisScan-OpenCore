import os
from core.base import BaseScanner

class NmapModule(BaseScanner):
    def __init__(self, target):
        super().__init__(target)

    def scan_services(self):
        self.logger.info(f"Running Nmap elite service scan for {self.target}...")
        host = self.sanitize_input(self.target)
        # Basic service scan: -sV (Service Version), -T4 (Aggressive timing)
        # WARNING: Aggressive timing (-T4) can cause network congestion and alert IDS/IPS.
        # Use mainly for internal CTFs or authorized ranges.
        cmd = ["nmap", "-sV", "-T4", host]
        return self.execute_hardened(cmd, tool_name="nmap")

class TrafficScanner(BaseScanner):
    def __init__(self, target):
        super().__init__(target)

    def capture_analysis(self, duration=15):
        self.logger.info(f"Starting Elite passive traffic analysis via Tshark ({duration}s)...")
        # Monitor for cleartext protocols: HTTP, FTP, Telnet, SMTP
        cmd = ["tshark", "-a", f"duration:{duration}", "-Y", "http or ftp or telnet or smtp", "-T", "fields", "-e", "frame.protocols", "-e", "ip.src", "-e", "ip.dst"]
        return self.execute_hardened(cmd, tool_name="tshark")


class ReconModule(BaseScanner):
    def __init__(self, target):
        super().__init__(target)
        self.nmap = NmapModule(target)

    def detect_stack(self):
        self.logger.info(f"Detecting technology stack for {self.target}...")
        results = {
            "cms": None,
            "server": None,
            "language": None,
            "frameworks": [],
            "nmap_output": ""
        }
        
        try:
            if "wordpress" in self.target.lower():
                results["cms"] = "WordPress"
            
            # Use Go-based fast scanner if available (Reference Implementation content)
            host = self.sanitize_input(self.target)
            # UPDATED: Moved to examples/ for Open-Core compliance
            go_bin = "examples/fast_port_scanner_demo"
            if os.name == 'nt': go_bin += ".exe"
            
            if os.path.exists(go_bin):
                self.logger.info("Using Go-based reference scanner (Demo)...")
                results["go_scan_output"] = self.execute_hardened([os.path.abspath(go_bin), host])
            else:
                 self.logger.debug("Go-based reference scanner not compiled/found in examples/")
            
            # Use active nmap scan
            results["nmap_output"] = self.nmap.scan_services()
            
        except Exception as e:
            self.logger.error(f"Detection failed: {str(e)}")
            
        return results

class VulnerabilityScanner(BaseScanner):
    def __init__(self, target):
        super().__init__(target)

    def run_nuclei(self):
        self.logger.info("Running Nuclei scans...")
        # Simulated nuclei command
        # cmd = ["nuclei", "-u", self.target, "-t", "cves/", "-severity", "critical,high,medium"]
        # return self.execute_command(cmd)
        return [] # Placeholder

    def run_nikto(self):
        self.logger.info("Running Nikto scans...")
        # cmd = ["nikto", "-h", self.target]
        # return self.execute_command(cmd)
        return [] # Placeholder
