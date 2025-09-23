#!/usr/bin/env python3
import subprocess
from datetime import datetime
import time
import sys
import platform


def ping_host(host, timeout=1):
    """Ping a host and return True if reachable, False otherwise."""
    # Use appropriate ping command based on OS
    if platform.system().lower() == "windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), host]
    else:
        cmd = ["ping", "-c", "1", "-W", str(timeout), host]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout + 1
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def monitor_host(host):
    """Monitor host status and display changes with duration."""
    current_status = None
    status_start_time = None

    print(f"Monitoring {host}...")

    try:
        while True:
            is_up = ping_host(host)
            current_time = time.time()

            # First check - establish initial state
            if current_status is None:
                current_status = is_up
                status_start_time = current_time

            # Status changed
            elif current_status != is_up:
                duration = int(current_time - status_start_time)
                status_word = "up" if current_status else "down"
                time_now = datetime.now().strftime("%H:%M:%S")
                print(
                    f"\r{host} was {status_word} for {duration} seconds until {time_now}"
                )

                current_status = is_up
                status_start_time = current_time

            # Status unchanged - update inline counter
            duration = int(current_time - status_start_time)
            status_word = "up" if current_status else "down"
            print(
                f"\r{host} is now {status_word} for {duration} seconds",
                end="",
                flush=True,
            )

            time.sleep(1)

    except KeyboardInterrupt:
        duration = int(time.time() - status_start_time)
        status_word = "up" if current_status else "down"
        print(f"\r{host} was {status_word} for {duration} seconds")
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python host_monitor.py <host_ip_or_hostname>")
        sys.exit(1)

    host = sys.argv[1]
    monitor_host(host)
