from collections import deque


def simulate_fifo(reference_string, num_frames):
    frames = [None] * num_frames
    fifo_queue = deque()

    page_faults = 0
    page_hits = 0

    print("FIFO Page Replacement")
    print("-" * 55)
    print("Step\tPage\tFrames\t\tStatus")
    print("-" * 55)

    for step, page in enumerate(reference_string, start=1):

        if page in frames:
            page_hits += 1
            status = "Hit"

        else:
            page_faults += 1
            status = "Fault"

            if None in frames:
                index = frames.index(None)
            else:
                index = fifo_queue.popleft()

            frames[index] = page
            fifo_queue.append(index)

        print(f"{step}\t{page}\t{frames}\t{status}")

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

    simulate_fifo(reference_string, num_frames)
