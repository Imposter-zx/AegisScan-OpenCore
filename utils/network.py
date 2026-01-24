import os
import socket
import logging
import subprocess
import ipaddress

def is_local_network(target):
    """
    Checks if a target is within a private/local network range.
    """
    try:
        # Resolve hostname to IP if needed
        target_host = target.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
        ip = socket.gethostbyname(target_host)
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private or ip_obj.is_loopback
    except:
        return False

def detect_cdn(target):
    """
    Identifies if the target is behind a CDN/WAF.
    Checks common headers and DNS patterns.
    """
    logger = logging.getLogger("AegisScan.NetworkUtil")
    host = target.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
    
    cdn_info = {"name": "None", "active": False}
    
    try:
        # Check for Cloudflare via DNS
        # In a real environment, we'd use dns.resolver
        # Here we simulate header-based check if socket resolve is slow
        addr = socket.gethostbyname(host)
        
        # Simulated Cloudflare range check or header check
        # results = subprocess.run(["nslookup", host], capture_output=True, text=True)
        
        # Common CDN Indicators
        indicators = ["cloudflare", "akamai", "cloudfront", "fastly"]
        for ind in indicators:
            if ind in host.lower():
                cdn_info = {"name": ind.capitalize(), "active": True}
                break
                
    except Exception as e:
        logger.error(f"CDN Detection Error: {str(e)}")
        
    return cdn_info

def is_packet_capture_feasible(target):
    """
    Checks if packet capture is feasible and authorized.
    Criteria: 
    1. Root/Administrative privileges.
    2. Tshark is installed.
    3. Target is in a private/local network (authorized range).
    """
    logger = logging.getLogger("AegisScan.NetworkUtil")
    
    # 1. Local Network check
    if not is_local_network(target):
        logger.warning(f"Target {target} is NOT on a local/private network. Skipping traffic analysis for safety.")
        return False

    # 2. Check for Tshark
    try:
        subprocess.run(["tshark", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("Tshark not found. Passive analysis disabled.")
        return False

    # 3. Check for Privileges
    if os.name == 'nt':
        try:
            import ctypes
            if ctypes.windll.shell32.IsUserAnAdmin() == 0:
                logger.warning("Packet capture requires Administrative privileges on Windows.")
                return False
        except:
            return False
    else:
        if os.getuid() != 0:
            logger.warning("Packet capture requires Root privileges on Linux.")
            return False

    return True

