"""
REST API Wrapper for AegisScan Strategic v4.0
Provides programmatic access to the AegisScan engine for integration with other tools.
"""

import threading
import time
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
import logging
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import main as run_aegisscan
from core.engine import ScanningEngine
from core.config import Config
from core.mission import MissionTypes

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Store active scans
active_scans: Dict[str, Any] = {}
scan_results: Dict[str, Any] = {}


def run_scan_async(
    scan_id: str,
    target: str,
    mode: str,
    mission: str,
    depth: int,
    interval: int,
    output_format: str,
    stealth: bool,
):
    """Run a scan in a separate thread"""
    try:
        engine = ScanningEngine(
            target=target,
            depth=depth,
            output_format=output_format,
            mode=mode,
            mission_type=getattr(MissionTypes, mission.upper()),
            stealth=stealth,
        )

        active_scans[scan_id] = {"status": "running", "start_time": time.time()}

        if interval > 0:
            # Continuous mode
            while active_scans.get(scan_id, {}).get("status") == "running":
                engine.run()
                time.sleep(interval * 60)
        else:
            # Single run
            engine.run()

        active_scans[scan_id]["status"] = "completed"
        active_scans[scan_id]["end_time"] = time.time()

    except Exception as e:
        active_scans[scan_id] = {"status": "failed", "error": str(e)}
        app.logger.error(f"Scan {scan_id} failed: {str(e)}")


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "aegisscan-api"})


@app.route("/scan", methods=["POST"])
def start_scan():
    """Start a new scan"""
    data = request.get_json()

    # Validate required parameters
    if not data or "target" not in data:
        return jsonify({"error": "Target is required"}), 400

    target = data["target"]
    mode = data.get("mode", Config.MODE_AUDIT)
    mission = data.get("mission", "RECON")
    depth = data.get("depth", 1)
    interval = data.get("interval", 0)
    output_format = data.get("output_format", "json")
    stealth = data.get("stealth", False)

    # Validate mode
    try:
        Config.validate_mode(mode)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Generate scan ID
    import hashlib

    scan_id = hashlib.md5(f"{target}{time.time()}".encode()).hexdigest()[:8]

    # Start scan in background thread
    thread = threading.Thread(
        target=run_scan_async,
        args=(scan_id, target, mode, mission, depth, interval, output_format, stealth),
    )
    thread.daemon = True
    thread.start()

    return jsonify(
        {
            "scan_id": scan_id,
            "status": "started",
            "target": target,
            "mode": mode,
            "mission": mission,
        }
    ), 202


@app.route("/scan/<scan_id>", methods=["GET"])
def get_scan_status(scan_id: str):
    """Get status of a scan"""
    if scan_id not in active_scans:
        return jsonify({"error": "Scan not found"}), 404

    return jsonify(active_scans[scan_id])


@app.route("/scans", methods=["GET"])
def list_scans():
    """List all scans"""
    return jsonify({"scans": active_scans})


@app.route("/scan/<scan_id>", methods=["DELETE"])
def stop_scan(scan_id: str):
    """Stop a running scan"""
    if scan_id not in active_scans:
        return jsonify({"error": "Scan not found"}), 404

    if active_scans[scan_id]["status"] == "running":
        active_scans[scan_id]["status"] = "stopped"
        return jsonify({"status": "stopped", "scan_id": scan_id})
    else:
        return jsonify({"error": "Scan is not running"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
