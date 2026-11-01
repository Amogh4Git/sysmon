import psutil


def get_cpu_metrics() -> dict:
    """Collects system CPU utilization, per-core utilization, core count, and clock frequency."""
    try:
        freq = psutil.cpu_freq()
        freq_mhz = round(freq.current, 2) if freq else None
    except (NotImplementedError, FileNotFoundError, PermissionError):
        freq_mhz = None

    return {
        "cpu_percent": float(psutil.cpu_percent(interval=None)),
        "per_core_percent": psutil.cpu_percent(interval=None, percpu=True),
        "cpu_count": psutil.cpu_count(logical=True) or 1,
        "frequency_mhz": freq_mhz,
    }


if __name__ == "__main__":
    print("[CPU Metrics Standalone Test Output]\n", get_cpu_metrics())
