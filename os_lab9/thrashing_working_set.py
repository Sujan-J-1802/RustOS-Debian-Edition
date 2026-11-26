def simulate_lru(pages, capacity):
    frames = []
    faults = 0
    hits = 0

    for page in pages:
        if page in frames:
            hits += 1
            frames.remove(page)

        else:
            faults += 1

            if len(frames) == capacity:
                frames.pop(0)

        frames.append(page)

    return faults, hits


def working_set(pages, window_size):
    return set(pages[-window_size:])


if __name__ == "__main__":
    pages = [1, 2, 3, 4, 5] * 4
    window_size = 5

    ws = working_set(pages, window_size)

    print("Thrashing and Working-Set Simulation")
    print("=" * 65)

    print("Reference String:", pages)
    print("Total References:", len(pages))
    print("Working Set Window:", window_size)
    print("Working Set:", sorted(ws))
    print("Working Set Size:", len(ws))

    print("-" * 65)

    print(f"{'Frames':<10}{'Faults':<10}{'Hits':<10}"
          f"{'Fault Rate':<15}{'Status'}")

    print("-" * 65)

    for capacity in range(1, 7):
        faults, hits = simulate_lru(pages, capacity)

        fault_rate = faults / len(pages) * 100

        if capacity < len(ws) and fault_rate >= 80:
            status = "Thrashing"
        else:
            status = "Stable"

        rate = f"{fault_rate:.2f}%"

        print(f"{capacity:<10}{faults:<10}{hits:<10}"
              f"{rate:<15}{status}")

    print("-" * 65)

    print("Minimum frames required:", len(ws))
    print("Insufficient frames cause excessive page faults.")
