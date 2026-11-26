def simulate_optimal(reference_string, num_frames):
    frames = [None] * num_frames

    page_faults = 0
    page_hits = 0

    print("Optimal Page Replacement")
    print("-" * 55)
    print("Step\tPage\tFrames\t\tStatus")
    print("-" * 55)

    for i, page in enumerate(reference_string):

        if page in frames:
            page_hits += 1
            status = "Hit"

        else:
            page_faults += 1
            status = "Fault"

            if None in frames:
                index = frames.index(None)

            else:
                future = reference_string[i + 1:]
                next_use = []

                for p in frames:
                    if p in future:
                        next_use.append(future.index(p))
                    else:
                        next_use.append(float("inf"))

                index = next_use.index(max(next_use))

            frames[index] = page

        print(f"{i + 1}\t{page}\t{frames}\t{status}")

    total = len(reference_string)

    print("-" * 55)
    print("Total References:", total)
    print("Number of Frames:", num_frames)
    print("Page Faults:", page_faults)
    print("Page Hits:", page_hits)
    print(f"Fault Rate: {page_faults / total * 100:.2f}%")
    print(f"Hit Rate: {page_hits / total * 100:.2f}%")


if __name__ == "__main__":
    reference_string = [
        7, 0, 1, 2, 0, 3, 0,
        4, 2, 3, 0, 3, 2
    ]

    num_frames = 3

    simulate_optimal(reference_string, num_frames)
