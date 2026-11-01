import os
import time
import psutil

_last_io, _last_time = None, None


def get_io_metrics(target_path: str = None) -> dict:
    """Collects disk capacity utilization and real-time read/write I/O throughput."""
    global _last_io, _last_time
    path = target_path or (os.path.splitdrive(os.getcwd())[0] + "\\" if os.name == "nt" else "/")
    try:
        d = psutil.disk_usage(path)
        disk_pct, total, used, free = float(d.percent), int(d.total), int(d.used), int(d.free)
    except (PermissionError, FileNotFoundError, OSError):
        disk_pct = total = used = free = None

    now = time.time()
    read_speed = write_speed = 0.0
    try:
        io = psutil.disk_io_counters()
        read_b, write_b = (int(io.read_bytes), int(io.write_bytes)) if io else (None, None)
        if _last_io and _last_time and io and now > _last_time:
            dt = now - _last_time
            read_speed = max(0.0, (read_b - _last_io[0]) / dt)
            write_speed = max(0.0, (write_b - _last_io[1]) / dt)
        if io:
            _last_io, _last_time = (read_b, write_b), now
    except (PermissionError, NotImplementedError, RuntimeError):
        read_b = write_b = None

    return {
        "primary_disk_percent": disk_pct,
        "total_bytes": total,
        "used_bytes": used,
        "free_bytes": free,
        "bytes_read": read_b,
        "bytes_written": write_b,
        "read_bytes_sec": read_speed,
        "write_bytes_sec": write_speed,
    }


if __name__ == "__main__":
    print("[Disk & I/O Metrics Output]\n", get_io_metrics())
