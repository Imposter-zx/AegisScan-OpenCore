# AegisScan Strategic v4.0

### Mission-Aware Adversarial Simulation Framework

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![Status: Open-Core](https://img.shields.io/badge/Status-Open--Core-green)](docs/STRATEGY.md)

**AegisScan Strategic** is a research-focused adversarial simulation framework designed for **Purple Teams**, **Security Defenders**, and **Educational Cyber Ranges**. Unlike traditional scanners that purely enumerate vulnerabilities, AegisScan simulates "mission-oriented" threat actor behavior—including phases of reconnaissance, validation, and objective emulation—to help organizations test their detection capabilities.

> [!WARNING]
> **Authorized Use Only**: This tool is for defensive research and authorized security assessments. Usage against targets without explicit written permission is illegal. See [ETHICS.md](ETHICS.md) for details.

---

## 🛡️ Why AegisScan?

Most security tools blast network traffic indiscriminately. **AegisScan** introduces the concept of **Strategic Missions**:

- **ROI-Aware Logic**: The engine disengages if the "cost" (risk of detection) exceeds the "value" of the target.
- **Mission Profiles**: Pre-defined logic for `RECON`, `VALIDATION`, or `EMULATION`.
- **Defensive Focus**: Designed to generate realistic noise patterns for SOC training.

## 📂 Repository Structure (Open-Core)

This repository follows a Responsible Open-Core model ([Read Strategy](docs/STRATEGY.md)):

- `core/`: The heart of the framework (Engine, Intelligence, Reporting).
- `modules/`: Standard wrappers for assessment tools (Nmap, various scanners).
- `examples/`: Reference implementations for educational study (e.g., `fast_port_scanner_demo.go`).
- `reports/`: output location for JSON/Text mission reports.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Nmap / Tshark (optional, for specific modules)
- Go (optional, for compiling example scanners)

### Installation

```bash
git clone https://github.com/Imposter-zx/AegisScan-OpenCore
cd AegisScan-OpenCore
pip install -r requirements.txt  # If applicable
```

### Usage

**Standard Audit Mode (Safe):**

```bash
python main.py target.com --mode audit --mission recon
```

**Continuous Observation (Blue Team Training):**

```bash
python main.py target.com --interval 60 --mode observation
```

## ⚖️ License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.
This ensures that any modifications—even if run as a network service—must remain open source. We believe this prevents the weaponization of our research in closed, commercial attack platforms.

See [LICENSE](LICENSE) for the full text.

---

_Created for the Advancement of Defensive Security Research._
