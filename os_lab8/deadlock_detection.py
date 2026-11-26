"""Deadlock Detection Simulation (Multi-instance Resource Allocation)."""

from __future__ import annotations
import time


class DeadlockDetector:
    def __init__(
        self,
        available: list[int],
        allocation: list[list[int]],
        request: list[list[int]],
    ) -> None:
        self.available = list(available)
        self.allocation = [list(row) for row in allocation]
        self.request = [list(row) for row in request]
        self.num_processes = len(allocation)
        self.num_resources = len(available)

    def detect(self) -> tuple[list[int], list[int], float]:
        """Returns (completed_order, deadlocked_pids, elapsed_ms)."""

        start = time.perf_counter()

        work = list(self.available)

        # Step 1: Finish[i] = False if Allocation[i] != 0 else True
        finish = [
            all(val == 0 for val in self.allocation[i])
            for i in range(self.num_processes)
        ]

        completed_order: list[int] = [
            i for i, done in enumerate(finish) if done
        ]

        # Step 2: Find an index i such that Finish[i] == False and Request[i] <= Work
        while True:
            progressed = False
            for i in range(self.num_processes):
                if not finish[i] and all(
                    self.request[i][j] <= work[j]
                    for j in range(self.num_resources)
                ):
                    # Step 3: Reclaim resources upon simulated completion
                    for j in range(self.num_resources):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    completed_order.append(i)
                    progressed = True

            if not progressed:
                break

        # Step 4: Any process with Finish[i] == False is deadlocked
        deadlocked = [i for i, done in enumerate(finish) if not done]

        elapsed_ms = (time.perf_counter() - start) * 1000
        return completed_order, deadlocked, elapsed_ms

    def print_report(self, title: str) -> None:
        print(f"\n=== {title} ===")
        print(f"Available Vector: {self.available}\n")
        print(f"{'PID':<6} {'Allocation':<14} {'Current Request':<16}")
        print("-" * 44)

        for i in range(self.num_processes):
            print(
                f"P{i:<5} | {str(self.allocation[i]):<14} | "
                f"{str(self.request[i]):<16}"
            )

        completed, deadlocked, elapsed_ms = self.detect()

        print(f"\nDetection Latency: {elapsed_ms:.4f} ms")
        print(
            f"Completion Order : "
            f"{' -> '.join(f'P{p}' for p in completed) or 'None'}"
        )

        if deadlocked:
            dl_str = ", ".join(f"P{p}" for p in deadlocked)
            print(f"Status           : DEADLOCK DETECTED")
            print(f"Deadlocked Set   : {{{dl_str}}}")
        else:
            print(f"Status           : NO DEADLOCK (All processes can finish)")


def main() -> None:
    print("Deadlock Detection Simulation")
    print("=" * len("Deadlock Detection Simulation"))

    # Classic 5-process, 3-resource snapshot (Total instances: A=7, B=2, C=6)
    available = [0, 0, 0]
    allocation = [
        [0, 1, 0],  # P0
        [2, 0, 0],  # P1
        [3, 0, 2],  # P2
        [2, 1, 1],  # P3
        [0, 0, 2],  # P4
    ]

    # Scenario A: No deadlock (P0 and P2 finish first and release resources)
    request_ok = [
        [0, 0, 0],  # P0
        [2, 0, 2],  # P1
        [0, 0, 0],  # P2
        [1, 0, 2],  # P3
        [0, 0, 2],  # P4
    ]

    detector_ok = DeadlockDetector(available, allocation, request_ok)
    detector_ok.print_report("Scenario A: Resolvable State")

    # Scenario B: P2 requests 1 additional instance of C -> forms circular dependency
    request_deadlock = [
        [0, 0, 0],  # P0 finishes, releases (0, 1, 0)
        [2, 0, 2],  # P1 needs (2, 0, 2) -> blocked
        [0, 0, 1],  # P2 needs (0, 0, 1) -> blocked
        [1, 0, 2],  # P3 needs (1, 0, 2) -> blocked
        [0, 0, 2],  # P4 needs (0, 0, 2) -> blocked
    ]

    detector_dl = DeadlockDetector(available, allocation, request_deadlock)
    detector_dl.print_report("Scenario B: Deadlocked State")


if __name__ == "__main__":
    main()
