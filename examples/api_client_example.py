"""
Example client for interacting with the AegisScan API
"""

import requests
import time
import json
import sys

API_BASE = "http://localhost:5000"


def start_scan(
    target, mode="audit", mission="RECON", depth=1, interval=0, stealth=False
):
    """Start a new scan and return the scan ID"""
    try:
        response = requests.post(
            f"{API_BASE}/scan",
            json={
                "target": target,
                "mode": mode,
                "mission": mission,
                "depth": depth,
                "interval": interval,
                "stealth": stealth,
            },
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error starting scan: {e}")
        return None


def get_scan_status(scan_id):
    """Get the current status of a scan"""
    try:
        response = requests.get(f"{API_BASE}/scan/{scan_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting scan status: {e}")
        return None


def list_scans():
    """List all scans"""
    try:
        response = requests.get(f"{API_BASE}/scans")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error listing scans: {e}")
        return None


def stop_scan(scan_id):
    """Stop a running scan"""
    try:
        response = requests.delete(f"{API_BASE}/scan/{scan_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error stopping scan: {e}")
        return None


def wait_for_completion(scan_id, timeout=300):
    """Wait for a scan to complete"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        status = get_scan_status(scan_id)
        if not status:
            print("Lost connection to API")
            return False

        current_status = status.get("status")
        print(f"Scan {scan_id} status: {current_status}")

        if current_status in ["completed", "failed", "stopped"]:
            return current_status == "completed"

        time.sleep(5)

    print(f"Timeout waiting for scan {scan_id} to complete")
    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python api_client_example.py <target> [mode] [mission]")
        print("Example: python api_client_example.py example.com audit RECON")
        sys.exit(1)

    target = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "audit"
    mission = sys.argv[3] if len(sys.argv) > 3 else "RECON"

    print(f"Starting scan of {target} with mode={mode}, mission={mission}")

    # Start the scan
    result = start_scan(target, mode=mode, mission=mission)
    if not result:
        sys.exit(1)

    scan_id = result.get("scan_id")
    print(f"Scan started with ID: {scan_id}")

    # Wait for completion
    if wait_for_completion(scan_id):
        print("Scan completed successfully!")

        # Get final status
        final_status = get_scan_status(scan_id)
        if final_status:
            print(f"Final status: {json.dumps(final_status, indent=2)}")
    else:
        print("Scan did not complete successfully")
        sys.exit(1)


if __name__ == "__main__":
    main()
