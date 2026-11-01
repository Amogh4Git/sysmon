import psutil


def get_ram_metrics():
    """Collects system RAM total, used, available (GB) and percent."""
    ram = psutil.virtual_memory()
    return {
        "total": round(ram.total / (1024 ** 3), 2),
        "used": round(ram.used / (1024 ** 3), 2),
        "available": round(ram.available / (1024 ** 3), 2),
        "percent": ram.percent,
    }


if __name__ == "__main__":
    data = get_ram_metrics()
    print("===== RAM MONITORING =====")
    print(f"Total RAM     : {data['total']} GB\nUsed RAM      : {data['used']} GB\nAvailable RAM : {data['available']} GB\nRAM Usage     : {data['percent']} %")
