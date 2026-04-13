# AegisScan Strategic v4.0 API Documentation

## Overview

AegisScan provides a RESTful API for programmatic access to its adversarial simulation capabilities. This enables integration with SIEM/SOAR platforms, orchestration tools, and custom security workflows.

## Base URL

```
http://localhost:5000
```

## Authentication

The API currently does not implement authentication. In production environments, it is recommended to place the API behind an authentication proxy or implement API key validation.

## Endpoints

### Health Check

**GET** `/health`

Check if the API service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "aegisscan-api"
}
```

### Start a Scan

**POST** `/scan`

Initiate a new scanning operation.

**Request Body:**
```json
{
  "target": "example.com",
  "mode": "audit",
  "mission": "RECON",
  "depth": 2,
  "interval": 0,
  "output_format": "json",
  "stealth": false
}
```

**Parameters:**
- `target` (string, required): Target host or IP address
- `mode` (string, optional): Operational mode (`audit`, `stealth`, `observation`). Default: `audit`
- `mission` (string, optional): Strategic mission (`RECON`, `VALIDATION`, `EMULATION`). Default: `RECON`
- `depth` (integer, optional): Scan depth level (1-3). Default: `1`
- `interval` (integer, optional): Scan interval in minutes for continuous mode. `0` for single run. Default: `0`
- `output_format` (string, optional): Output format (`text`, `json`, `both`). Default: `json`
- `stealth` (boolean, optional): Enable stealth mode. Default: `false`

**Response:**
```json
{
  "scan_id": "a1b2c3d4",
  "status": "started",
  "target": "example.com",
  "mode": "audit",
  "mission": "RECON"
}
```

**HTTP Status Codes:**
- `202`: Scan started successfully
- `400`: Invalid request parameters
- `500`: Internal server error

### Get Scan Status

**GET** `/scan/{scan_id}`

Retrieve the status of a specific scan.

**Parameters:**
- `scan_id` (string, required): The scan identifier returned when starting a scan

**Response:**
```json
{
  "scan_id": "a1b2c3d4",
  "status": "running",
  "start_time": 1640995200.0,
  "target": "example.com",
  "mode": "audit",
  "mission": "RECON"
}
```

**Possible status values:**
- `starting`: Scan is initializing
- `running`: Scan is actively executing
- `completed`: Scan has finished successfully
- `failed`: Scan encountered an error
- `stopped`: Scan was manually stopped

**HTTP Status Codes:**
- `200`: Status retrieved successfully
- `404`: Scan not found

### List All Scans

**GET** `/scans`

Retrieve status of all scans.

**Response:**
```json
{
  "scans": {
    "a1b2c3d4": {
      "status": "completed",
      "start_time": 1640995200.0,
      "end_time": 1640995500.0,
      "target": "example.com"
    },
    "e5f6g7h8": {
      "status": "running",
      "start_time": 1640995800.0,
      "target": "test.example.com"
    }
  }
}
```

### Stop a Scan

**DELETE** `/scan/{scan_id}`

Stop a running scan.

**Parameters:**
- `scan_id` (string, required): The scan identifier to stop

**Response:**
```json
{
  "status": "stopped",
  "scan_id": "a1b2c3d4"
}
```

**HTTP Status Codes:**
- `200`: Scan stopped successfully
- `400`: Scan is not running
- `404`: Scan not found

## Integration Examples

### Python Client Example

```python
import requests
import time
import json

API_BASE = "http://localhost:5000"

def start_scan(target, mode="audit", mission="RECON"):
    """Start a new scan and return the scan ID"""
    response = requests.post(
        f"{API_BASE}/scan",
        json={
            "target": target,
            "mode": mode,
            "mission": mission
        }
    )
    response.raise_for_status()
    return response.json()["scan_id"]

def get_scan_status(scan_id):
    """Get the current status of a scan"""
    response = requests.get(f"{API_BASE}/scan/{scan_id}")
    response.raise_for_status()
    return response.json()

# Example usage
scan_id = start_scan("example.com", "audit", "RECON")
print(f"Started scan: {scan_id}")

# Poll for completion
while True:
    status = get_scan_status(scan_id)
    print(f"Scan status: {status['status']}")
    
    if status["status"] in ["completed", "failed", "stopped"]:
        break
        
    time.sleep(5)

print("Scan finished!")
```

### Bash/cURL Example

```bash
# Start a scan
SCAN_ID=$(curl -s -X POST http://localhost:5000/scan \
  -H "Content-Type: application/json" \
  -d '{"target":"example.com","mode":"audit","mission":"RECON"}' | \
  jq -r '.scan_id')

echo "Started scan: $SCAN_ID"

# Check status until complete
while true; do
  STATUS=$(curl -s http://localhost:5000/scan/$SCAN_ID | jq -r '.status')
  echo "Status: $STATUS"
  
  if [[ "$STATUS" =~ ^(completed|failed|stopped)$ ]]; then
    break
  fi
  
  sleep 5
done

echo "Scan finished!"
```

## Webhook Integration

AegisScan can be configured to send results to a webhook endpoint upon scan completion. Configure this in `config.yaml`:

```yaml
integrations:
  webhook:
    enabled: true
    url: "https://your-siem.example.com/webhook/aegisscan"
    headers:
      Authorization: "Bearer your-token-here"
      Content-Type: "application/json"
    template: "default"
```

## Error Responses

All error responses follow this format:

```json
{
  "error": "Description of the error"
}
```

Common error codes:
- `400`: Bad Request - Invalid parameters
- `404`: Not Found - Resource not found
- `500`: Internal Server Error - Unexpected error

## Rate Limiting

The API does not currently implement rate limiting. For production deployments, consider placing the API behind a rate-limiting proxy or implementing application-level rate limiting.

## Security Considerations

1. **Network Exposure**: The API binds to `0.0.0.0:5000` by default. In production, restrict access using firewall rules or bind to localhost only.
2. **Input Validation**: While basic validation is performed, always validate and sanitize inputs in your integration code.
3. **Scan Targets**: Ensure you have proper authorization before scanning any targets.
4. **Data Sensitivity**: Scan results may contain sensitive information. Consider encryption for transit and storage.

## Changelog

### v4.0.0
- Initial API release
- RESTful endpoints for scan management
- Background thread processing for async operations
- Basic health check and status endpoints