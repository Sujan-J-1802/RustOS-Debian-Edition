import os


def get_process_info(pid):

    try:

        process = {
            "PID": pid,
            "Name": "Unknown",
            "State": "Unknown",
            "PPid": "0",
            "Threads": "0",
            "VmRSS": "0 kB"
        }

        with open(f"/proc/{pid}/status", "r") as file:

            for line in file:

                key, separator, value = line.partition(":")

                if key in process:
                    process[key] = value.strip()

        return process

    except (FileNotFoundError, PermissionError, ProcessLookupError):

        return None


def list_processes():

    processes = []

    for entry in os.listdir("/proc"):

        if entry.isdigit():

            process = get_process_info(entry)

            if process:
                processes.append(process)

    processes.sort(key=lambda p: int(p["PID"]))

    return processes


def display_processes(processes):

    print("\n===== RUNNING SYSTEM PROCESSES =====")

    print(f"{'PID':<8}"
          f"{'NAME':<20}"
          f"{'STATE':<5}"
          f"{'PPID':<8}"
          f"{'THREADS':<10}"
          f"{'MEMORY':<15}")

    print("-" * 66)
import os


def get_process_info(pid):

    try:

        process = {
            "PID": pid,
            "Name": "Unknown",
            "State": "Unknown",
            "PPid": "0",
            "Threads": "0",
            "VmRSS": "0 kB"
        }

        with open(f"/proc/{pid}/status", "r") as file:

            for line in file:

                key, separator, value = line.partition(":")

                if key in process:
                    process[key] = value.strip()

        return process

    except (FileNotFoundError, PermissionError, ProcessLookupError):

        return None


def list_processes():

    processes = []

    for entry in os.listdir("/proc"):

        if entry.isdigit():

            process = get_process_info(entry)

            if process:
                processes.append(process)

    processes.sort(key=lambda p: int(p["PID"]))

    return processes


def display_processes(processes):

    print("\n===== RUNNING SYSTEM PROCESSES =====")

    print(f"{'PID':<8}"
          f"{'NAME':<20}"
          f"{'STATE':<5}"
          f"{'PPID':<8}"
          f"{'THREADS':<10}"
          f"{'MEMORY':<15}")

    print("-" * 66)

    for process in processes:

        print(f"{process['PID']:<8}"
              f"{process['Name'][:19]:<20}"
              f"{process['State'][0]:<5}"
              f"{process['PPid']:<8}"
              f"{process['Threads']:<10}"
              f"{process['VmRSS']:<15}")


def inspect_process(pid):

    process = get_process_info(pid)

    if process is None:

        print("Process not found or access denied")

        return

    print("\n===== DETAILED PROCESS INFORMATION =====")

    print("Process ID:", process["PID"])
    print("Process Name:", process["Name"])
    print("Process State:", process["State"])
    print("Parent Process ID:", process["PPid"])
    print("Number of Threads:", process["Threads"])
    print("Memory Usage:", process["VmRSS"])

    try:

        with open(f"/proc/{pid}/cmdline", "rb") as file:

            command = file.read().replace(
                b"\x00", b" "
            ).decode(errors="replace").strip()

            print("Command Line:", command or "Unavailable")

    except OSError:

        print("Command line unavailable")

    try:

        executable = os.readlink(f"/proc/{pid}/exe")

        print("Executable Path:", executable)

    except OSError:

        print("Executable path unavailable")


if __name__ == "__main__":

    print("Linux Process Inspection using /proc")
    print("=" * 66)

    if not os.path.isdir("/proc"):

        print("Error: Linux /proc file system not found")
        raise SystemExit(1)

    processes = list_processes()

    print("Total Processes Detected:", len(processes))

    # Display first 15 processes
    display_processes(processes[:15])

    # Inspect current Python process
    current_pid = os.getpid()

    print("\nCurrent Python Process ID:", current_pid)

    inspect_process(current_pid)

    # Inspect a user-selected process
    pid = input("\nEnter PID to inspect: ").strip()

    if pid.isdigit():

        inspect_process(pid)

    else:

        print("Invalid Process ID")

    print("\nProcess inspection completed successfully.")
    for process in processes:

        print(f"{process['PID']:<8}"
              f"{process['Name'][:19]:<20}"
              f"{process['State'][0]:<5}"
              f"{process['PPid']:<8}"
              f"{process['Threads']:<10}"
              f"{process['VmRSS']:<15}")


def inspect_process(pid):

    process = get_process_info(pid)

    if process is None:

        print("Process not found or access denied")

        return

    print("\n===== DETAILED PROCESS INFORMATION =====")

    print("Process ID:", process["PID"])
    print("Process Name:", process["Name"])
    print("Process State:", process["State"])
    print("Parent Process ID:", process["PPid"])
    print("Number of Threads:", process["Threads"])
    print("Memory Usage:", process["VmRSS"])

    try:

        with open(f"/proc/{pid}/cmdline", "rb") as file:

            command = file.read().replace(
                b"\x00", b" "
            ).decode(errors="replace").strip()

            print("Command Line:", command or "Unavailable")

    except OSError:

        print("Command line unavailable")

    try:

        executable = os.readlink(f"/proc/{pid}/exe")

        print("Executable Path:", executable)

    except OSError:

        print("Executable path unavailable")


if __name__ == "__main__":

    print("Linux Process Inspection using /proc")
    print("=" * 66)

    if not os.path.isdir("/proc"):

        print("Error: Linux /proc file system not found")
        raise SystemExit(1)

    processes = list_processes()

    print("Total Processes Detected:", len(processes))

    # Display first 15 processes
    display_processes(processes[:15])

    # Inspect current Python process
    current_pid = os.getpid()

    print("\nCurrent Python Process ID:", current_pid)

    inspect_process(current_pid)

    # Inspect a user-selected process
    pid = input("\nEnter PID to inspect: ").strip()

    if pid.isdigit():

        inspect_process(pid)

    else:

        print("Invalid Process ID")

    print("\nProcess inspection completed successfully.")
