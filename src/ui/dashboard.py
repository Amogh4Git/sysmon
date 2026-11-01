import os
import time
from colorama import Fore, Style, init

init(autoreset=True)

STATUS_COLORS = {
    "NORMAL": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "CRITICAL": Fore.RED,
}


def _fmt_rate(b):
    return f"{b / (1024 ** 2):.1f} MB/s" if b >= 1024 ** 2 else f"{b / 1024:.1f} KB/s"


class DashboardLogger:

    def _get_status_color(self, state):
        """Returns ANSI colored text based on state string, dictionary, or tuple."""
        if isinstance(state, dict):
            state = state.get("state", "UNKNOWN")
        elif isinstance(state, (tuple, list)):
            state = state[0] if state else "UNKNOWN"
        state = str(state).upper() if state else "UNKNOWN"
        color = STATUS_COLORS.get(state)
        return f"{color}{Style.BRIGHT}{state}{Style.RESET_ALL}" if color else state

    def render_dashboard(self, cpu_data, ram_data, io_data, health_data) -> None:
        """Clears terminal screen and renders live system metrics."""
        os.system("cls" if os.name == "nt" else "clear")

        state = health_data.get("state", "UNKNOWN") if isinstance(health_data, dict) else (health_data[0] if isinstance(health_data, (tuple, list)) and health_data else health_data)
        reasons = health_data.get("reasons", []) if isinstance(health_data, dict) else (health_data[1] if isinstance(health_data, (tuple, list)) and len(health_data) > 1 else [])

        cpu_pct = (cpu_data.get("cpu_percent") if isinstance(cpu_data, dict) else cpu_data) or 0.0
        ram_pct = (ram_data.get("percent") if isinstance(ram_data, dict) else ram_data) or 0.0
        disk_pct = (io_data.get("primary_disk_percent") if isinstance(io_data, dict) else io_data) or 0.0

        used_gb = (io_data.get("used_bytes") / (1024 ** 3)) if isinstance(io_data, dict) and io_data.get("used_bytes") else None
        tot_gb = (io_data.get("total_bytes") / (1024 ** 3)) if isinstance(io_data, dict) and io_data.get("total_bytes") else None
        space_str = f" ({used_gb:.1f}/{tot_gb:.1f} GB)" if used_gb and tot_gb else ""

        print("==================================================")
        print("          SYSTEM HEALTH MONITOR DASHBOARD         ")
        print("==================================================")
        print(f" Timestamp  : {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f" Status     : {self._get_status_color(state)}")
        print("--------------------------------------------------")
        print(f" CPU Usage  : {cpu_pct:>5.1f}%")
        print(f" RAM Usage  : {ram_pct:>5.1f}%")
        print(f" Disk Space : {disk_pct:>5.1f}%{space_str}")
        if isinstance(io_data, dict) and ("read_bytes_sec" in io_data or "write_bytes_sec" in io_data):
            print(f" Disk I/O   : R: {_fmt_rate(io_data.get('read_bytes_sec', 0)):<9} | W: {_fmt_rate(io_data.get('write_bytes_sec', 0))}")

        if reasons:
            print("--------------------------------------------------\n Status Notes:")
            for r in reasons:
                print(f"  - {r}")

        print("==================================================")
        print(" Press Ctrl+C to stop monitoring.")


_ui_instance = DashboardLogger()


def render_dashboard(cpu, ram, io, health):
    _ui_instance.render_dashboard(cpu, ram, io, health)
