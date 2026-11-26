"""Dining Philosophers Simulation demonstrating deadlock avoidance via resource ordering."""

from __future__ import annotations
import argparse
import random
import threading
import time
from dataclasses import dataclass


@dataclass
class PhilosopherStats:
    meals_eaten: int = 0
    total_wait_time: float = 0.0


class DiningTable:
    def __init__(self, count: int) -> None:
        self.count = count
        self.forks = [threading.Lock() for _ in range(count)]
        self.stats = [PhilosopherStats() for _ in range(count)]

    def dine(self, phil_id: int, meals: int) -> None:
        left = phil_id
        right = (phil_id + 1) % self.count

        # Deadlock avoidance: always acquire lower-indexed fork first
        first_fork, second_fork = sorted((left, right))

        for meal in range(1, meals + 1):
            # Thinking
            print(f"Philosopher {phil_id} Thinking...")
            time.sleep(random.uniform(0.01, 0.1))

            # Competing for forks
            start_wait = time.perf_counter()
            with self.forks[first_fork]:
                print(f"Philosopher {phil_id} Picked up fork {first_fork}")
                with self.forks[second_fork]:
                    print(f"Philosopher {phil_id} Picked up fork {second_fork}")
                    wait_duration = time.perf_counter() - start_wait
                    self.stats[phil_id].total_wait_time += wait_duration

                    # Eating
                    print(
                        f" ---> Philosopher {phil_id} EATING "
                        f"(Meal {meal}/{meals}) <---"
                    )
                    time.sleep(random.uniform(0.05, 0.15))
                    self.stats[phil_id].meals_eaten += 1

            print(
                f"Philosopher {phil_id} Put down forks "
                f"({first_fork}, {second_fork})"
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Dining Philosophers Simulation"
    )
    parser.add_argument(
        "--philosophers",
        type=int,
        default=5,
        help="Number of philosophers (default: 5)"
    )
    parser.add_argument(
        "--meals",
        type=int,
        default=3,
        help="Meals per philosopher (default: 3)"
    )
    args = parser.parse_args()

    if args.philosophers < 2:
        parser.error("Number of philosophers must be at least 2")

    print("Dining Philosophers Simulation")
    print("-" * 30)
    print(f"Philosophers={args.philosophers}, Meals/Phil={args.meals}")
    print("Strategy: Strict Resource Ordering (Low Index -> High Index)\n")

    table = DiningTable(args.philosophers)

    threads = [
        threading.Thread(target=table.dine, args=(i, args.meals))
        for i in range(args.philosophers)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("\nSimulation complete. Metrics summary:")
    print("-" * 50)
    print(
        f"{'Philosopher':<14} | {'Meals Eaten':<12} | "
        f"{'Total Wait (ms)':<15}"
    )
    print("-" * 50)

    for i, stat in enumerate(table.stats):
        print(
            f"{i:<14} | {stat.meals_eaten:<12} | "
            f"{stat.total_wait_time * 1000:<15.2f}"
        )


if __name__ == "__main__":
    main()
