import sys
import time

SAMPLING_INTERVAL = 2  # Sampling delay in seconds


def main():
    """Main execution loop for system resource monitoring."""
    print(f"Starting System Resource Monitor...\nSampling every {SAMPLING_INTERVAL} seconds. Press Ctrl+C to stop.\n")

    from src.metrics.cpu_metrics import get_cpu_metrics
    from src.metrics.ram_metrics import get_ram_metrics
    from src.metrics.io_metrics import get_io_metrics
    from src.health.classifier import evaluate_health
    from src.ui.dashboard import DashboardLogger

    ui = DashboardLogger()

    try:
        while True:
            cpu, ram, io = get_cpu_metrics(), get_ram_metrics(), get_io_metrics()
            ui.render_dashboard(cpu, ram, io, evaluate_health(cpu, ram, io))
            time.sleep(SAMPLING_INTERVAL)
    except KeyboardInterrupt:
        print("\n[INFO] Monitoring process stopped cleanly by user (Ctrl+C). Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred during monitoring: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
