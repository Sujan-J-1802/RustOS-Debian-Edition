def simulate(requests, algorithm):

    if algorithm == "FCFS":
        queue = requests.copy()

    elif algorithm == "SJF":
        queue = sorted(requests, key=lambda x: x[1])

    elif algorithm == "Priority":
        queue = sorted(requests, key=lambda x: x[2])

    current_time = 0
    total_waiting = 0
    total_completion = 0

    print("\nAlgorithm:", algorithm)
    print("-" * 65)

    print(f"{'Request':<12}{'Service':<12}{'Priority':<12}"
          f"{'Waiting':<12}{'Completion'}")

    for request, service_time, priority in queue:

        waiting_time = current_time
        current_time += service_time
        completion_time = current_time

        total_waiting += waiting_time
        total_completion += completion_time

        print(f"{request:<12}{service_time:<12}{priority:<12}"
              f"{waiting_time:<12}{completion_time}")

    average_waiting = total_waiting / len(queue)
    average_completion = total_completion / len(queue)

    print("-" * 65)

    print("Service Order:", " -> ".join(r[0] for r in queue))
    print(f"Average Waiting Time: {average_waiting:.2f} ms")
    print(f"Average Completion Time: {average_completion:.2f} ms")
    print(f"Total Execution Time: {current_time} ms")

    return average_waiting, average_completion


if __name__ == "__main__":

    # Request ID, Service Time, Priority
    requests = [
        ("R1", 8, 3),
        ("R2", 4, 1),
        ("R3", 9, 4),
        ("R4", 2, 2),
        ("R5", 5, 5)
    ]

    print("I/O Request Scheduling Simulation")
    print("=" * 65)

    results = {}

    for algorithm in ["FCFS", "SJF", "Priority"]:
        results[algorithm] = simulate(requests, algorithm)

    print("\nPerformance Comparison")
    print("=" * 65)

    print(f"{'Algorithm':<15}{'Avg Waiting':<20}"
          f"{'Avg Completion'}")

    for name, (waiting, completion) in results.items():
        print(f"{name:<15}{waiting:<20.2f}{completion:.2f}")

    best = min(results, key=lambda x: results[x][0])

    print("-" * 65)
    print("Best Performing Algorithm:", best)
