from collections import deque


def buffering():
    buffer = deque()
    capacity = 3
    produced = 0
    consumed = 0
    time = 0
    total_items = 10

    print("\n===== BUFFERING SIMULATION =====")

    while consumed < total_items:
        time += 1

        if produced < total_items and len(buffer) < capacity:
            produced += 1
            buffer.append(produced)
            print(f"Time {time}: Produced item {produced}")

        if time % 2 == 0 and buffer:
            item = buffer.popleft()
            consumed += 1
            print(f"Time {time}: Consumed item {item}")

    print("Total items processed:", consumed)
    print("Total time:", time, "units")
    print(f"Throughput: {consumed / time:.2f} items/unit")


def caching():
    cache = {}
    requests = [1, 2, 1, 3, 2, 4, 1, 3]

    hits = 0
    misses = 0
    time = 0

    print("\n===== CACHING SIMULATION =====")

    for request in requests:
        if request in cache:
            hits += 1
            time += 1
            print(f"Request {request}: Cache Hit")

        else:
            misses += 1
            time += 5
            cache[request] = f"Data {request}"
            print(f"Request {request}: Cache Miss")

    print("Total requests:", len(requests))
    print("Cache hits:", hits)
    print("Cache misses:", misses)
    print(f"Hit rate: {hits / len(requests) * 100:.2f}%")
    print("Time without cache:", len(requests) * 5, "units")
    print("Time with cache:", time, "units")
    print(f"Throughput: {len(requests) / time:.2f} requests/unit")


def spooling():
    spool = deque()

    jobs = [
        ("Document1", 3),
        ("Document2", 2),
        ("Document3", 4),
        ("Document4", 1)
    ]

    time = 0

    print("\n===== SPOOLING SIMULATION =====")

    for job in jobs:
        spool.append(job)
        print(f"{job[0]} added to print queue")

    print("\nProcessing print queue:")

    while spool:
        document, duration = spool.popleft()

        print(f"Time {time}: Printing {document}")

        time += duration

        print(f"Time {time}: Completed {document}")

    print("Total documents printed:", len(jobs))
    print("Total printing time:", time, "units")
    print(f"Throughput: {len(jobs) / time:.2f} jobs/unit")


if __name__ == "__main__":
    print("Buffering, Caching and Spooling Simulation")
    print("=" * 55)

    buffering()
    caching()
    spooling()

    print("\nSimulation completed successfully.")
