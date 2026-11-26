from collections import deque


def fifo(pages, capacity):
    frames = deque()
    faults = 0

    for page in pages:
        if page not in frames:
            faults += 1

            if len(frames) == capacity:
                frames.popleft()

            frames.append(page)

    return faults


def lru(pages, capacity):
    frames = []
    faults = 0

    for page in pages:
        if page in frames:
            frames.remove(page)

        else:
            faults += 1

            if len(frames) == capacity:
                frames.pop(0)

        frames.append(page)

    return faults


def optimal(pages, capacity):
    frames = []
    faults = 0

    for i, page in enumerate(pages):
        if page not in frames:
            faults += 1

            if len(frames) < capacity:
                frames.append(page)

            else:
                future = pages[i + 1:]
                next_use = []

                for p in frames:
                    if p in future:
                        next_use.append(future.index(p))
                    else:
                        next_use.append(float("inf"))

                index = next_use.index(max(next_use))
                frames[index] = page

    return faults


if __name__ == "__main__":
    pages = [
        7, 0, 1, 2, 0, 3, 0,
        4, 2, 3, 0, 3, 2
    ]

    capacity = 3
    total = len(pages)

    results = {
        "FIFO": fifo(pages, capacity),
        "LRU": lru(pages, capacity),
        "Optimal": optimal(pages, capacity)
    }

    print("Page Replacement Algorithm Comparison")
    print("=" * 65)

    print("Reference String:", pages)
    print("Number of Frames:", capacity)
    print("Total References:", total)

    print("-" * 65)

    print(f"{'Algorithm':<12}{'Faults':<10}{'Hits':<10}"
          f"{'Fault Rate':<15}{'Hit Rate':<15}")

    print("-" * 65)

    for algorithm, faults in results.items():
        hits = total - faults
        fault_rate = faults / total * 100
        hit_rate = hits / total * 100

        print(f"{algorithm:<12}{faults:<10}{hits:<10}"
              f"{fault_rate:<14.2f}%{hit_rate:.2f}%")

    print("-" * 65)

    best = min(results, key=results.get)

    print("Best Performing Algorithm:", best)
    print("Minimum Page Faults:", results[best])
