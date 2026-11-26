import os
import time


def get_cpu_times():

    with open("/proc/stat", "r") as file:

        values = file.readline().split()[1:9]

    values = list(map(int, values))

    idle = values[3] + values[4]
    total = sum(values)

    return idle, total


def get_cpu_usage():

    idle1, total1 = get_cpu_times()

    time.sleep(1)

    idle2, total2 = get_cpu_times()

    idle_difference = idle2 - idle1
    total_difference = total2 - total1

    if total_difference == 0:
        return 0

    usage = 100 * (
        1 - idle_difference / total_difference
    )

    return usage


def get_memory_usage():

    memory = {}

    with open("/proc/meminfo", "r") as file:

        for line in file:

            key, value = line.split(":", 1)

            memory[key] = int(value.split()[0])

    total = memory["MemTotal"]
    available = memory["MemAvailable"]
    used = total - available

    usage = (used / total) * 100

    return total, used, available, usage


def get_process_information():

    processes = []

    for pid in os.listdir("/proc"):

        if pid.isdigit():

            try:

                with open(
                    f"/proc/{pid}/status", "r"
                ) as file:

                    data = {}

                    for line in file:

                        key, separator, value = \
                            line.partition(":")

                        data[key] = value.strip()

                name = data.get("Name", "Unknown")
                state = data.get("State", "?")

                memory = int(
                    data.get("VmRSS", "0 kB").split()[0]
                )

                processes.append(
                    (pid, name, state, memory)
                )

            except OSError:

                continue

    return processes


def get_uptime():

    with open("/proc/uptime", "r") as file:

        uptime = float(file.read().split()[0])

    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)

    return hours, minutes, seconds


def display_resources():

    cpu_usage = get_cpu_usage()

    total, used, available, memory_usage = \
        get_memory_usage()

    processes = get_process_information()

    hours, minutes, seconds = get_uptime()

    print("\n===== CPU INFORMATION =====")

    print("Logical CPU Count:", os.cpu_count())
    print(f"CPU Usage: {cpu_usage:.2f}%")

    print("\n===== MEMORY INFORMATION =====")

    print(f"Total Memory: {total / 1024:.2f} MB")
    print(f"Used Memory: {used / 1024:.2f} MB")
    print(f"Available Memory: {available / 1024:.2f} MB")
    print(f"Memory Usage: {memory_usage:.2f}%")

    print("\n===== SYSTEM INFORMATION =====")

    print(f"Uptime: {hours}h {minutes}m {seconds}s")
    print("Total Processes:", len(processes))

    print("\n===== TOP 5 MEMORY-USING PROCESSES =====")

    processes.sort(
        key=lambda process: process[3],
        reverse=True
    )

    print(f"{'PID':<10}{'NAME':<20}"
          f"{'STATE':<10}{'MEMORY (MB)':<15}")

    print("-" * 55)

    for pid, name, state, memory in processes[:5]:

        print(f"{pid:<10}{name[:19]:<20}"
              f"{state[0]:<10}{memory / 1024:<15.2f}")


if __name__ == "__main__":

    if not os.path.isfile("/proc/stat"):

        print("Error: This program requires Linux")
        raise SystemExit(1)

    print("Linux System Resource Monitor")
    print("=" * 55)

    try:

        while True:

            os.system("clear")

            print("Linux System Resource Monitor")
            print("=" * 55)

            display_resources()

            print("\nPress Ctrl+C to stop monitoring")

            time.sleep(2)

    except KeyboardInterrupt:

        print("\nResource monitoring stopped.")
