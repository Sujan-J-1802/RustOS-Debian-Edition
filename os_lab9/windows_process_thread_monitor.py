import os
import csv
import time
import subprocess
import threading


def get_processes():

    result = subprocess.check_output(
        ["tasklist", "/FO", "CSV", "/NH"],
        text=True,
        errors="replace"
    )

    processes = []

    for row in csv.reader(result.splitlines()):

        if len(row) >= 5:

            processes.append({
                "Name": row[0],
                "PID": row[1],
                "Session": row[2],
                "SessionNumber": row[3],
                "Memory": row[4]
            })

    return processes


def display_processes():

    processes = get_processes()

    print("\n===== WINDOWS PROCESS INFORMATION =====")

    print("Total Processes:", len(processes))

    print(f"\n{'PID':<10}"
          f"{'PROCESS NAME':<30}"
          f"{'SESSION':<15}"
          f"{'MEMORY':<15}")

    print("-" * 70)

    for process in processes[:15]:

        print(f"{process['PID']:<10}"
              f"{process['Name'][:29]:<30}"
              f"{process['Session']:<15}"
              f"{process['Memory']:<15}")


def inspect_process(pid):

    print("\n===== SELECTED PROCESS INFORMATION =====")

    result = subprocess.check_output(
        ["tasklist", "/FI", f"PID eq {pid}", "/V"],
        text=True,
        errors="replace"
    )

    print(result)


def worker(stop_event):

    stop_event.wait()


def thread_monitor():

    print("\n===== THREAD MONITORING =====")

    print("Current Process ID:", os.getpid())
    print("Main Thread ID:", threading.get_native_id())

    stop_event = threading.Event()

    threads = []

    for i in range(1, 4):

        thread = threading.Thread(
            target=worker,
            args=(stop_event,),
            name=f"Worker-{i}"
        )

        threads.append(thread)

        thread.start()

    print("\nActive Python Threads:",
          threading.active_count())

    print(f"\n{'THREAD NAME':<20}"
          f"{'THREAD ID':<15}"
          f"{'STATUS':<15}")

    print("-" * 50)

    for thread in threading.enumerate():

        status = "ALIVE" if thread.is_alive() else "STOPPED"

        print(f"{thread.name:<20}"
              f"{str(thread.native_id):<15}"
              f"{status:<15}")

    time.sleep(1)

    # Signal all worker threads to finish
    stop_event.set()

    for thread in threads:

        thread.join()

        print(f"{thread.name} completed")

    print("\nRemaining Active Python Threads:",
          threading.active_count())


if __name__ == "__main__":

    print("Windows Process and Thread Monitor")
    print("=" * 70)

    if os.name != "nt":

        print("Error: This program requires Windows")
        raise SystemExit(1)

    print("Operating System:", os.name)
    print("Logical CPU Count:", os.cpu_count())
    print("Current Python Process ID:", os.getpid())

    # Display Windows processes
    display_processes()

    # Inspect current Python process
    inspect_process(os.getpid())

    # Demonstrate multithreading
    thread_monitor()

    print("\nMonitoring completed successfully.")
