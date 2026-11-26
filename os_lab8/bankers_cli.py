"""Recommended OS lab: Banker's Algorithm (Extended Interactive Simulation)."""

from __future__ import annotations

import argparse
import copy
import time


class BankersSystem:
    def __init__(
        self,
        available: list[int],
        maximum: list[list[int]],
        allocation: list[list[int]],
    ) -> None:
        self.available = list(available)
        self.maximum = [list(row) for row in maximum]
        self.allocation = [list(row) for row in allocation]
        self.n_proc = len(allocation)
        self.n_res = len(available)

    @property
    def need(self) -> list[list[int]]:
        return [
            [self.maximum[i][j] - self.allocation[i][j] for j in range(self.n_res)]
            for i in range(self.n_proc)
        ]

    def is_safe(self) -> tuple[bool, list[int], float]:
        start_time = time.perf_counter()
        work = list(self.available)
        finish = [False] * self.n_proc
        need_mat = self.need
        sequence: list[int] = []

        while len(sequence) < self.n_proc:
            progressed = False
            for p in range(self.n_proc):
                if not finish[p] and all(
                    need_mat[p][r] <= work[r] for r in range(self.n_res)
                ):
                    for r in range(self.n_res):
                        work[r] += self.allocation[p][r]
                    finish[p] = True
                    sequence.append(p)
                    progressed = True

            if not progressed:
                elapsed = (time.perf_counter() - start_time) * 1000
                return False, [], elapsed

        elapsed = (time.perf_counter() - start_time) * 1000
        return True, sequence, elapsed

    def request(self, pid: int, req: list[int]) -> bool:
        if pid < 0 or pid >= self.n_proc:
            print(f"Error: Invalid process ID P{pid}.")
            return False

        if len(req) != self.n_res:
            print(f"Error: Request vector must have {self.n_res} elements.")
            return False

        need_mat = self.need

        if any(req[r] > need_mat[pid][r] for r in range(self.n_res)):
            print(
                f" [DENIED] P{pid} request {req} exceeds declared Need {need_mat[pid]}."
            )
            return False

        if any(req[r] > self.available[r] for r in range(self.n_res)):
            print(
                f" [WAIT] P{pid} request {req} exceeds Available {self.available}."
            )
            return False

        prev_avail = copy.deepcopy(self.available)
        prev_alloc = copy.deepcopy(self.allocation)

        for r in range(self.n_res):
            self.available[r] -= req[r]
            self.allocation[pid][r] += req[r]

        safe, seq, elapsed_ms = self.is_safe()

        if safe:
            seq_fmt = " -> ".join(f"P{p}" for p in seq)
            print(
                f" [GRANTED] Safe sequence: {seq_fmt} "
                f"(checked in {elapsed_ms:.4f} ms)"
            )
            return True
        else:
            self.available = prev_avail
            self.allocation = prev_alloc
            print(
                f" [DENIED] Allocation leads to UNSAFE state "
                f"(checked in {elapsed_ms:.4f} ms). Rolled back."
            )
            return False

    def display(self) -> None:
        need_mat = self.need
        print(f"\nAvailable: {self.available}")
        print(f"{'PID':<6} {'Allocation':<14} {'Max':<14} {'Need':<14}")
        print("-" * 56)

        for p in range(self.n_proc):
            print(
                f"P{p:<5} | {str(self.allocation[p]):<14} | "
                f"{str(self.maximum[p]):<14} | {str(need_mat[p]):<14}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Banker's Algorithm Simulation")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Enter interactive mode to submit custom resource requests",
    )
    args = parser.parse_args()

    print("Banker's Algorithm")
    print("=" * len("Banker's Algorithm"))

    system = BankersSystem(
        available=[3, 3, 2],
        maximum=[
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3],
        ],
        allocation=[
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2],
        ],
    )

    system.display()
    safe, seq, elapsed_ms = system.is_safe()
    print(
        f"\nInitial State: {'SAFE' if safe else 'UNSAFE'} "
        f"(Safety check: {elapsed_ms:.4f} ms)"
    )

    if safe:
        print(f"Safe Sequence: {' -> '.join(f'P{p}' for p in seq)}")

    if args.interactive:
        print("\nInteractive Mode: Enter <pid> <r0> <r1> <r2> or 'q' to quit.")

        while True:
            raw = input("\nRequest > ").strip()

            if raw.lower() in ("q", "quit", "exit"):
                break

            try:
                parts = [int(x) for x in raw.split()]
                pid, req = parts[0], parts[1:]
                system.request(pid, req)
                system.display()
            except (ValueError, IndexError):
                print("Invalid input. Format: <pid> <r0> <r1> <r2> (e.g., 1 1 0 2)")


if __name__ == "__main__":
    main()
