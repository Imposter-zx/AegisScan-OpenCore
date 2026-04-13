# Examples

This directory contains example code and integrations for AegisScan Strategic v4.0.

## Contents

1. **api_client_example.py** - A Python client demonstrating how to interact with the AegisScan REST API
2. **fast_port_scanner_demo.go** - Existing Go port scanner example (educational)
3. *(Add your own examples here)*

## API Client Example

The `api_client_example.py` script shows how to:
- Start a scan via the REST API
- Monitor scan progress
- Handle scan completion
- List active scans
- Stop running scans

### Usage

```bash
# Install requirements
pip install requests

# Run the example (make sure the API server is running)
python api_client_example.py example.com audit RECON
```

### Running the API Server

To use the API client example, first start the AegisScan API server:

```bash
# Install API dependencies
pip install flask

# Start the server
python api/server.py
```

The API will be available at http://localhost:5000

## Educational Examples

The existing `fast_port_scanner_demo.go` file is provided as an educational reference for understanding basic network scanning concepts in Go.