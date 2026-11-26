def head_movement(sequence, head):
    total = 0

    for track in sequence:
        total += abs(track - head)
        head = track

    return total


def fcfs(requests, head):
    return requests.copy()


def sstf(requests, head):
    pending = requests.copy()
    sequence = []

    while pending:
        nearest = min(pending, key=lambda x: abs(x - head))

        sequence.append(nearest)
        pending.remove(nearest)
        head = nearest

    return sequence


def scan(requests, head, disk_size):
    left = sorted([x for x in requests if x < head])
    right = sorted([x for x in requests if x >= head])

    return right + [disk_size - 1] + left[::-1]


def cscan(requests, head, disk_size):
    left = sorted([x for x in requests if x < head])
    right = sorted([x for x in requests if x >= head])

    return right + [disk_size - 1, 0] + left


def look(requests, head):
    left = sorted([x for x in requests if x < head])
    right = sorted([x for x in requests if x >= head])

    return right + left[::-1]


def clook(requests, head):
    left = sorted([x for x in requests if x < head])
    right = sorted([x for x in requests if x >= head])

    return right + left


if __name__ == "__main__":
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    head = 53
    disk_size = 200

    algorithms = {
        "FCFS": fcfs(requests, head),
        "SSTF": sstf(requests, head),
        "SCAN": scan(requests, head, disk_size),
        "C-SCAN": cscan(requests, head, disk_size),
        "LOOK": look(requests, head),
        "C-LOOK": clook(requests, head)
    }

    print("Disk Scheduling Algorithms")
    print("=" * 65)
    print("Request Queue:", requests)
    print("Initial Head Position:", head)
    print("Disk Size:", disk_size)
    print("Initial Direction: Right")
    print("=" * 65)

    results = {}

    for name, sequence in algorithms.items():
        movement = head_movement(sequence, head)
        results[name] = movement

        print("\nAlgorithm:", name)
        print("Head Path:", " -> ".join(
            map(str, [head] + sequence)
        ))
        print("Total Head Movement:", movement)

    print("\n" + "=" * 65)
    print("Performance Comparison")
    print("-" * 40)

    print(f"{'Algorithm':<15}{'Head Movement'}")

    for name, movement in results.items():
        print(f"{name:<15}{movement}")

    best = min(results, key=results.get)

    print("-" * 40)
    print("Best Performing Algorithm:", best)
    print("Minimum Head Movement:", results[best])
