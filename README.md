# AegisScan Strategic v4.0

### Mission-Aware Adversarial Simulation Framework

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![Status: Open-Core](https://img.shields.io/badge/Status-Open--Core-green)](docs/STRATEGY.md)
[![Focus: Defensive Research](https://img.shields.io/badge/Focus-Defensive_Research-purple.svg)](ETHICS.md)

**AegisScan Strategic** is a professional, research-focused adversarial simulation framework designed for **Purple Teams**, **Security Defenders**, and **Educational Cyber Ranges**.

Unlike traditional vulnerability scanners that purely enumerate flaws, AegisScan simulates "mission-oriented" threat actor behavior—incorporating phases of reconnaissance, validation, and objective emulation—to rigorously test and improve organization detection capabilities.

> [!IMPORTANT]
> **Research & Defense Only**: This framework is strictly for defensive security research, authorized security assessments, and educational purposes. It is designed to help organizations validate their defenses, not to exploit unauthorized systems.

---

## 🎯 Who This Is For

This framework is engineered for:

- **Blue Teams & SOC Analysts**: To generate realistic "attack noise" for tuning SIEM/EDR alerts.
- **Purple Teams**: To validate detection logic against specific adversarial behaviors.
- **Cyber Range Administrators**: To populate training environments with coherent, mission-driven traffic.
- **Security Researchers**: To study automated decision-making in adversarial contexts.

## ⛔ Who This Is NOT For

- **Unauthorized Actors**: The framework includes safety constraints and is not suitable for unauthorized offensive operations.
- **"Point-and-Click" Exploitation**: This is not a Metasploit alternative. It does not contain weaponized exploits or zero-days.

---

## 🛡️ Strategic Architecture

Most security tools blast network traffic indiscriminately. **AegisScan** introduces the concept of **Strategic Missions**:

- **ROI-Aware Decision Engine**: The system effectively "calibrates" itself; if the risk of detection (cost) outweighs the intelligence value (ROI) of a target, the engine disengages.
- **Mission Profiles**: Pre-defined logic sets for specific audit goals:
  - `RECON`: Passive and active information gathering.
  - `VALIDATION`: Safe confirmation of misconfigurations.
  - `EMULATION`: Replication of specific TTPs (Tactics, Techniques, and Procedures).
- **Defensive Focus**: Primed to generate realistic, attributable patterns that aid in SOC training and signature development.

---

## 📂 Repository Structure (Open-Core)

This repository follows a **Responsible Open-Core** research model (see [STRATEGY.md](docs/STRATEGY.md)):

- `core/`: The framework's engine, intelligence processing, and reporting subsystems.
- `modules/`: Standard wrappers for assessment tools (Nmap, various scanners) operating in safety modes.
- `examples/`: Educational reference implementations (e.g., `fast_port_scanner_demo.go`).
- `reports/`: output location for structured JSON/Text mission reports.

> **Note**: Aggressive evasion logic and weaponized modules are intentionally excluded from the open-core release to prevent misuse.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Nmap / Tshark (optional, for specific passive reconnaissance modules)
- Go (optional, for compiling example scanners)

### Installation

```bash
git clone https://github.com/Imposter-zx/AegisScan-OpenCore
cd AegisScan-OpenCore
pip install -r requirements.txt
```

### Usage

**Standard Audit Mode (Safe)**
Runs a mission simulation to identify exposure without aggressive probing.

```bash
python main.py target.com --mode audit --mission recon
```

**Continuous Observation (Detection Training)**
Runs periodic, low-volume activity to test continuous monitoring alertness.

```bash
python main.py target.com --interval 60 --mode observation
```

---

## ⚖️ Ethics & License

### Responsible Use

By using this software, you agree to the terms in [ETHICS.md](ETHICS.md). You strictly prohibited from using this tool against any target without explicit, written authorization.

### Open Source License

This project is released under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.
This ensures that the core research remains open and sets a barrier against the weaponization of this code in closed-source commercial attack platforms.

See [LICENSE](LICENSE) for the full text.

---

_Created for the Advancement of Defensive Security Research._
