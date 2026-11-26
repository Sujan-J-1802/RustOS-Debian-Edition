"""Readers-Writers Simulation using Python threading and Locks."""

from __future__ import annotations
import argparse
import random
import threading
import time


class ReadWriteLock:
    """First Readers-Writers synchronization lock (Reader-preference)."""

    def __init__(self) -> None:
        self.readers_count = 0
        self._mutex = threading.Lock()
        self._rw_lock = threading.Lock()

    def acquire_read(self) -> int:
        with self._mutex:
            self.readers_count += 1
            if self.readers_count == 1:
                self._rw_lock.acquire()  # Lock out writers
            return self.readers_count

    def release_read(self) -> int:
        with self._mutex:
            self.readers_count -= 1
            if self.readers_count == 0:
                self._rw_lock.release()  # Release lock for writers
            return self.readers_count

    def acquire_write(self) -> None:
        self._rw_lock.acquire()

    def release_write(self) -> None:
        self._rw_lock.release()


class SharedDatabase:
    def __init__(self, initial_val: int = 100) -> None:
        self.data = initial_val
        self.lock = ReadWriteLock()

    def read(self, reader_id: int) -> None:
        active = self.lock.acquire_read()
        print(
            f"[Reader {reader_id}] READ shared_data = {self.data} "
            f"(Active Readers: {active})"
        )
        time.sleep(random.uniform(0.01, 0.025))
        self.lock.release_read()

    def write(self, writer_id: int, increment: int) -> None:
        self.lock.acquire_write()
        self.data += increment
        print(
            f">> [Writer {writer_id}] MODIFIED shared_data to "
            f"{self.data} <<"
        )
        time.sleep(random.uniform(0.02, 0.04))
        self.lock.release_write()


def reader_task(db: SharedDatabase, reader_id: int, operations: int) -> None:
    for _ in range(operations):
        time.sleep(random.uniform(0.01, 0.03))
        db.read(reader_id)


def writer_task(db: SharedDatabase, writer_id: int, operations: int) -> None:
    for _ in range(operations):
        time.sleep(random.uniform(0.02, 0.05))
        db.write(writer_id, increment=10)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Readers-Writers Simulation"
    )
    parser.add_argument(
        "--readers", type=int, default=5,
        help="Number of reader threads"
    )
    parser.add_argument(
        "--writers", type=int, default=2,
        help="Number of writer threads"
    )
    parser.add_argument(
        "--ops", type=int, default=3,
        help="Number of operations per thread"
    )

    args = parser.parse_args()

    print("Readers-Writers Simulation")
    print("--------------------------")
    print(
        f"Readers={args.readers}, Writers={args.writers}, "
        f"Ops/Thread={args.ops}\n"
    )

    db = SharedDatabase()

    r_threads = [
        threading.Thread(
            target=reader_task,
            args=(db, i + 1, args.ops)
        )
        for i in range(args.readers)
    ]

    w_threads = [
        threading.Thread(
            target=writer_task,
            args=(db, i + 1, args.ops)
        )
        for i in range(args.writers)
    ]

    for t in r_threads:
        t.start()

    for t in w_threads:
        t.start()

    for t in r_threads:
        t.join()

    for t in w_threads:
        t.join()

    print(f"\nSimulation complete. Final shared_data = {db.data}")


if __name__ == "__main__":
    main()
