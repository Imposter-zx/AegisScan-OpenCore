#!/bin/bash

# AegisScan Bootstrap Script
# This script ensures the environment is set up and executes the scanner.

echo "------------------------------------------------------------"
echo "AegisScan: Automated Pentesting Tool"
echo "------------------------------------------------------------"

# 1. Check for Python
if ! command -v python3 &> /dev/null; then
    echo "[!] Error: Python3 is not installed."
    exit 1
fi

# 2. Check for required scanning tools
TOOLS=("nmap" "tshark" "nuclei")
for tool in "${TOOLS[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        echo "[!] Warning: $tool is not installed. Some features will be disabled."
    fi
done

# 3. Compile Go modules if Go is installed
if command -v go &> /dev/null; then
    echo "[*] Compiling high-performance Go modules..."
    go build -o modules/fast_scan modules/fast_scan.go
fi

# 4. Execute the Python core
echo "[*] Launching AegisScan v2.0 Enterprise Engine..."
python3 main.py "$@"
