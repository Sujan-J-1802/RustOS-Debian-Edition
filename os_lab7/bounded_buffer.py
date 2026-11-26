
#!/usr/bin/env python3
"""Bounded-Buffer Producer-Consumer Simulation using Python threading and Condition variables."""

from __future__ import annotations

import argparse
import random
import threading
import time
from typing import Any

SENTINEL = None


class BoundedBuffer:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.buffer: list[Any | None] = [None] * capacity
        self.in_idx = 0
        self.out_idx = 0
        self.count = 0

        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def insert(self, item: Any, producer_id: int) -> None:
        with self.not_full:
            while self.count == self.capacity:
                self.not_full.wait()

            self.buffer[self.in_idx] = item
            self.in_idx = (self.in_idx + 1) % self.capacity
            self.count += 1

            print(
                f"[Producer {producer_id}] Produced {item} | "
                f"Buffer count: {self.count}/{self.capacity}"
            )

            self.not_empty.notify()

    def remove(self, consumer_id: int) -> Any:
        with self.not_empty:
            while self.count == 0:
                self.not_empty.wait()

            item = self.buffer[self.out_idx]
            self.buffer[self.out_idx] = None
            self.out_idx = (self.out_idx + 1) % self.capacity
            self.count -= 1

            if item is not SENTINEL:
                print(
                    f"[Consumer {consumer_id}] Consumed {item} | "
                    f"Buffer count: {self.count}/{self.capacity}"
                )

            self.not_full.notify()
            return item


def producer_worker(
    buffer: BoundedBuffer,
    producer_id: int,
    items_to_produce: int
) -> None:
    for _ in range(items_to_produce):
        item = random.randint(1, 99)
        time.sleep(random.uniform(0.00, 0.02))
        buffer.insert(item, producer_id)


def consumer_worker(buffer: BoundedBuffer, consumer_id: int) -> None:
    while True:
        item = buffer.remove(consumer_id)

        if item is SENTINEL:
            break

        time.sleep(random.uniform(0.01, 0.03))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bounded-Buffer Simulation"
    )

    parser.add_argument(
        "--capacity",
        type=int,
        default=5,
        help="Buffer capacity"
    )

    parser.add_argument(
        "--producers",
        type=int,
        default=2,
        help="Number of producers"
    )

    parser.add_argument(
        "--consumers",
        type=int,
        default=2,
        help="Number of consumers"
    )

    parser.add_argument(
        "--items",
        type=int,
        default=6,
        help="Items per producer"
    )

    args = parser.parse_args()

    print("Bounded-Buffer Producer-Consumer Simulation")
    print("-" * 43)

    print(
        f"Capacity: {args.capacity}, "
        f"Producers: {args.producers}, "
        f"Consumers: {args.consumers}, "
        f"Items/Producer: {args.items}"
    )

    buffer = BoundedBuffer(args.capacity)

    producers = [
        threading.Thread(
            target=producer_worker,
            args=(buffer, i + 1, args.items)
        )
        for i in range(args.producers)
    ]

    consumers = [
        threading.Thread(
            target=consumer_worker,
            args=(buffer, i + 1)
        )
        for i in range(args.consumers)
    ]

    for t in consumers:
        t.start()

    for t in producers:
        t.start()

    for t in producers:
        t.join()

    # Poison pill to shut down consumers
    for _ in range(args.consumers):
        buffer.insert(SENTINEL, producer_id=0)

    for t in consumers:
        t.join()

    print("\nSimulation complete: All items processed.")


if __name__ == "__main__":
    main()
