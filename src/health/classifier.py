THRESHOLDS = {
    "cpu": {"warning": 70, "critical": 90},
    "ram": {"warning": 70, "critical": 90},
    "disk": {"warning": 80, "critical": 90},
}
LABELS = {"cpu": "CPU", "ram": "RAM", "disk": "Disk"}


class HealthResult(dict):
    """Dictionary supporting both key access ('state', 'reasons') and tuple unpacking."""
    def __iter__(self):
        yield self["state"]
        yield self["reasons"]


def check_metric(value, metric_name):
    limits = THRESHOLDS[metric_name]
    if value >= limits["critical"]:
        return "CRITICAL"
    return "WARNING" if value >= limits["warning"] else "NORMAL"


def evaluate_health(cpu, ram, disk):
    raw = {
        "cpu": cpu.get("cpu_percent") if isinstance(cpu, dict) else cpu,
        "ram": ram.get("percent") if isinstance(ram, dict) else ram,
        "disk": disk.get("primary_disk_percent") if isinstance(disk, dict) else disk,
    }

    statuses, alerts = {}, []
    for name, val in raw.items():
        val = 0.0 if val is None else val
        if isinstance(val, bool) or not isinstance(val, (int, float)) or not 0 <= val <= 100:
            raise ValueError(f"{name} usage must be between 0 and 100")

        status = check_metric(val, name)
        statuses[name] = status
        if status != "NORMAL":
            level = "Critical" if status == "CRITICAL" else "Warning"
            suffix = "too high" if status == "CRITICAL" else "high"
            alerts.append(f"{level}: {LABELS[name]} usage is {suffix}")

    overall = "CRITICAL" if "CRITICAL" in statuses.values() else ("WARNING" if "WARNING" in statuses.values() else "NORMAL")
    return HealthResult(state=overall, reasons=alerts)
