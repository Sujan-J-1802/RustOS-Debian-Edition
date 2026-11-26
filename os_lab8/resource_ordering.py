"""Recommended OS Lab: Deadlock Prevention by Resource Ordering."""

from __future__ import annotations

import argparse
import threading
import time

from dataclasses import dataclass


@dataclass
class RunMetrics:
    completed_ops: int = 0
    deadlocks_triggered: int = 0
    total_wait_ms: float = 0.0


def run_simulation(num_resources: int, iterations: int, enforce_order: bool) -> RunMetrics:
    locks = [threading.Lock() for _ in range(num_resources)]
    metrics = RunMetrics()
    metrics_lock = threading.Lock()
    abort_event = threading.Event()

    def worker(tid: int, res_a: int, res_b: int) -> None:
        # Enforce total ordering (R_i < R_j) when enabled
        first, second = sorted((res_a, res_b)) if enforce_order else (res_a, res_b)

        for step in range(1, iterations + 1):
            if abort_event.is_set():
                return

            t0 = time.perf_counter()
            if not locks[first].acquire(timeout=0.5):
                print(f"[Thread {tid}] TIMEOUT waiting for R{first} -> DEADLOCK!")
                with metrics_lock:
                    metrics.deadlocks_triggered += 1
                abort_event.set()
                return

            try:
                # When race window is small two cycle threads hold their first lock simultaneously
                time.sleep(0.015)

                if not locks[second].acquire(timeout=0.5):
                    print(f"[Thread {tid}] TIMEOUT waiting for R{second} while holding R{first} -> DEADLOCK!")
                    with metrics_lock:
                        metrics.deadlocks_triggered += 1
                    abort_event.set()
                    return

                try:
                    wait_ms = (time.perf_counter() - t0) * 1000
                    time.sleep(0.005)  # Simulate critical section work
                    with metrics_lock:
                        metrics.completed_ops += 1
                        metrics.total_wait_ms += wait_ms
                finally:
                    locks[second].release()
            finally:
                locks[first].release()

    # Build cyclic dependency pairs: (0,1), (1,2), ..., (N-1, 0)
    threads = [
        threading.Thread(target=worker, args=(i, i, (i + 1) % num_resources))
        for i in range(num_resources)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Deadlock Prevention by Resource Ordering")
    parser.add_argument("--resources", type=int, default=4, help="Number of shared resources/threads (default: 4)")
    parser.add_argument("--iterations", type=int, default=5, help="Iterations per thread (default: 5)")
    args = parser.parse_args()

    print("Deadlock Prevention by Resource Ordering")
    print("=" * len("Deadlock Prevention by Resource Ordering"))
    print(f"Configuration: Resources/Threads={args.resources}, Iterations/Thread={args.iterations}\n")

    # 1. Unordered execution (Circular Wait possible)
    print("\n[1] Running WITHOUT global resource ordering (cyclic requests)...")
    m_unordered = run_simulation(args.resources, args.iterations, enforce_order=False)

    # 2. Globally ordered execution (Circular Wait prevented)
    print("\n[2] Running WITH global resource ordering (Strict R_i < R_j)...")
    m_ordered = run_simulation(args.resources, args.iterations, enforce_order=True)

    # Summary Table
    total_expected = args.resources * args.iterations
    print("\nMeasurement Summary:")
    print("-" * 60)
    print(f"{'Strategy':<22} | {'Completed Ops':<15} | {'Deadlocks':<10} | {'Avg Wait (ms)':<13}")
    print("-" * 60)

    avg_unordered = (m_unordered.total_wait_ms / m_unordered.completed_ops) if m_unordered.completed_ops else 0.0
    avg_ordered = (m_ordered.total_wait_ms / m_ordered.completed_ops) if m_ordered.completed_ops else 0.0

    print(f"{'Unordered (Cyclic)':<22} | {m_unordered.completed_ops:<15} | {m_unordered.deadlocks_triggered:<10} | {avg_unordered:.2f}")
    print(f"{'Ordered (R_i < R_j)':<22} | {m_ordered.completed_ops:<15} | {m_ordered.deadlocks_triggered:<10} | {avg_ordered:.2f}")

if __name__ == "__main__":
    main()

