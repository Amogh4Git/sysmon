# System Resource Monitor (sysmon)

A lightweight Python utility that continuously monitors CPU, RAM, and disk usage, classifies system health (NORMAL, WARNING, CRITICAL), displays a live terminal dashboard, and optionally logs metrics.

---
## Quick Start
```bash
# 1. Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows PowerShell
# source venv/bin/activate   # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the monitor
python main.py
```
Press **Ctrl+C** to stop.

---
## Project Structure
```
sysmon/
├─ src/                 # Core modules
│   ├─ metrics/          # CPU, RAM, Disk/I/O collectors
│   ├─ health/           # Threshold evaluation & classification
│   └─ ui/               # Terminal dashboard
├─ logs/                # Runtime CSV logs (auto‑generated)
├─ main.py              # Orchestrator & sampling loop
├─ requirements.txt     # Dependencies (psutil, colorama)
└─ README.md            # You are reading it!
```

---
## How It Works
1. **Metrics** – `src/metrics/*.py` gather raw percentages using `psutil`.
2. **Classification** – `src/health/classifier.py` checks values against warning/critical thresholds and returns a `HealthResult` containing `state` and `reasons`.
3. **Dashboard** – `src/ui/dashboard.py` renders a coloured, real‑time view in the terminal, showing CPU, RAM, disk space, and I/O throughput.
4. **Loop** – `main.py` repeats the above every `SAMPLING_INTERVAL` seconds (default 2 s).

---
## Configuration
Thresholds are defined in `src/health/classifier.py`:
```python
THRESHOLDS = {
    "cpu": {"warning": 70, "critical": 90},
    "ram": {"warning": 70, "critical": 90},
    "disk": {"warning": 80, "critical": 90},
}
```
Adjust the values as needed; the monitoring loop will pick them up automatically.

---


