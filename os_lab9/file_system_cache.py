from collections import OrderedDict


def simulate_cache(requests, capacity):

    cache = OrderedDict()
    hits = 0
    misses = 0

    print("-" * 55)
    print(f"{'Request':<12}{'Status':<12}{'Cache Contents'}")
    print("-" * 55)

    for block in requests:

        if block in cache:
            hits += 1
            status = "Hit"
            cache.move_to_end(block)

        else:
            misses += 1
            status = "Miss"

            if len(cache) == capacity:
                cache.popitem(last=False)

            cache[block] = f"Data Block {block}"

        print(f"{block:<12}{status:<12}{list(cache.keys())}")

    total = len(requests)
    hit_rate = hits / total * 100
    miss_rate = misses / total * 100

    print("-" * 55)
    print("Total Requests:", total)
    print("Cache Hits:", hits)
    print("Cache Misses:", misses)
    print(f"Hit Rate: {hit_rate:.2f}%")
    print(f"Miss Rate: {miss_rate:.2f}%")

    return hits, misses, hit_rate


if __name__ == "__main__":

    capacity = 3

    patterns = {
        "Sequential Access": [1, 2, 3, 4, 5, 6, 7, 8],
        "Repeated Access": [1, 2, 3, 1, 2, 3, 1, 2],
        "Mixed Access": [1, 2, 1, 4, 2, 5, 1, 2]
    }

    print("File-System Cache Simulation")
    print("=" * 55)
    print("Cache Capacity:", capacity)
    print("Replacement Policy: LRU")

    results = {}

    for name, requests in patterns.items():

        print("\nAccess Pattern:", name)
        print("Requests:", requests)

        results[name] = simulate_cache(requests, capacity)

    print("\n===== PERFORMANCE COMPARISON =====")

    print(f"{'Access Pattern':<22}{'Hits':<8}"
          f"{'Misses':<10}{'Hit Rate'}")

    print("-" * 55)

    for name, (hits, misses, rate) in results.items():

        print(f"{name:<22}{hits:<8}{misses:<10}{rate:.2f}%")

    print("\nSimulation completed successfully.")
