
"""Recommended OS Lab: Fixed Partition Memory Allocation. This is a pedagogical simulation/user-space demonstration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class Partition:
    partition_id: int
    size_kb: int
    allocated_pid: int | None = None
    process_size_kb: int = 0

    @property
    def is_free(self) -> bool:
        return self.allocated_pid is None

    @property
    def internal_fragmentation_kb(self) -> int:
        if self.is_free:
            return 0
        return self.size_kb - self.process_size_kb


@dataclass
class ProcessRequest:
    pid: str
    size_kb: int


class FixedPartitionAllocator:
    """Simulate static (fixed-size) contiguous memory partitioning (MFT)."""

    def __init__(
        self,
        partition_sizes_kb: list[int],
        strategy: Literal["first_fit", "best_fit"] = "first_fit",
    ) -> None:
        self.partitions = [
            Partition(partition_id=i, size_kb=size)
            for i, size in enumerate(partition_sizes_kb)
        ]
        self.strategy = strategy
        self.rejected_processes: list[tuple[ProcessRequest, str]] = []

    @property
    def total_memory_kb(self) -> int:
        return sum(p.size_kb for p in self.partitions)

    @property
    def total_internal_fragmentation_kb(self) -> int:
        return sum(p.internal_fragmentation_kb for p in self.partitions)

    @property
    def total_allocated_process_kb(self) -> int:
        return sum(
            p.process_size_kb for p in self.partitions if not p.is_free
        )

    @property
    def total_free_partition_kb(self) -> int:
        return sum(
            p.size_kb for p in self.partitions if p.is_free
        )

    def allocate(self, req: ProcessRequest) -> bool:
        candidates = [
            p for p in self.partitions
            if p.is_free and p.size_kb >= req.size_kb
        ]

        if not candidates:
            max_part = max(
                (p.size_kb for p in self.partitions), default=0
            )
            reason = (
                f"Exceeds largest partition ({max_part} KB)"
                if req.size_kb > max_part
                else "No free partition large enough available"
            )
            self.rejected_processes.append((req, reason))
            return False

        if self.strategy == "best_fit":
            chosen = min(
                candidates,
                key=lambda p: p.size_kb - req.size_kb
            )
        else:
            chosen = candidates[0]

        chosen.allocated_pid = req.pid
        chosen.process_size_kb = req.size_kb
        return True

    def deallocate(self, pid: str) -> bool:
        for p in self.partitions:
            if p.allocated_pid == pid:
                p.allocated_pid = None
                p.process_size_kb = 0
                return True
        return False

    def print_report(self, scenario_name: str) -> None:
        print(f"\n{'=' * 74}")
        print(f"Scenario: {scenario_name}")
        print(
            f"Strategy: {self.strategy.upper()} | "
            f"Total Physical Memory: {self.total_memory_kb} KB"
        )
        print(f"{'-' * 74}")
        print(
            f"{'Part ID':<9} | {'Capacity':<10} | {'Status':<10} | "
            f"{'Process':<9} | {'Used':<10} | {'Internal Frag.':<14}"
        )
        print("-" * 74)

        for p in self.partitions:
            status = "FREE" if p.is_free else "ALLOCATED"
            pid_str = p.allocated_pid if p.allocated_pid else "-"
            used_str = (
                f"{p.process_size_kb} KB" if not p.is_free else "-"
            )
            frag_str = (
                f"{p.internal_fragmentation_kb} KB"
                if not p.is_free else "-"
            )
            print(
                f"{p.partition_id:<9} | {p.size_kb:<10} KB | "
                f"{status:<10} | {pid_str:<9} | "
                f"{used_str:<10} | {frag_str:<14}"
            )

        print("-" * 74)

        utilization = (
            self.total_allocated_process_kb / self.total_memory_kb
        ) * 100
        frag_pct = (
            self.total_internal_fragmentation_kb / self.total_memory_kb
        ) * 100

        print(
            f"Summary: Used = {self.total_allocated_process_kb} KB "
            f"(Utilization: {utilization:.1f}%) | "
            f"Internal Frag. = {self.total_internal_fragmentation_kb} KB "
            f"({frag_pct:.1f}%) | "
            f"Unallocated Free = {self.total_free_partition_kb} KB"
        )
        print("=" * 74)

        if self.rejected_processes:
            print("Rejected:")
            for req, reason in self.rejected_processes:
                print(f" - {req.pid} ({req.size_kb} KB): {reason}")


def run_workload(
    name: str,
    partitions: list[int],
    requests: list[ProcessRequest],
    strategy: Literal["first_fit", "best_fit"],
) -> None:
    allocator = FixedPartitionAllocator(partitions, strategy=strategy)
    for req in requests:
        allocator.allocate(req)
    allocator.print_report(name)


def main() -> None:
    print("Fixed Partition Memory Allocation")
    print("=" * len("Fixed Partition Memory Allocation"))

    # Fixed partition layout: 5 static partitions totaling 1600 KB
    partition_layout = [100, 200, 300, 400, 600]

    # Scenario 1: Balanced workload (closely matching partition sizes)
    balanced_requests = [
        ProcessRequest("Proc_A", 95),
        ProcessRequest("Proc_B", 190),
        ProcessRequest("Proc_C", 285),
        ProcessRequest("Proc_D", 390),
        ProcessRequest("Proc_E", 500),
    ]
    run_workload(
        "1. Balanced Workload (Optimal Fit)",
        partition_layout,
        balanced_requests,
        "first_fit"
    )

    # Scenario 2: Small processes skew (many small partitions)
    # -> severe internal fragmentation
    small_skew_requests = [
        ProcessRequest("Proc_1", 40),
        ProcessRequest("Proc_2", 55),
        ProcessRequest("Proc_3", 60),
        ProcessRequest("Proc_4", 75),
        ProcessRequest("Proc_5", 90),
    ]
    run_workload(
        "2. Small-Process Skew (High Internal Fragmentation)",
        partition_layout,
        small_skew_requests,
        "first_fit"
    )

    # Scenario 3: Mixed contention & oversized process
    # (comparison First-Fit vs Best-Fit)
    mixed_requests = [
        ProcessRequest("Job_1", 100),
        ProcessRequest("Job_2", 550),
        ProcessRequest("Job_3", 700),  # Exceeds max partition (600 KB) -> rejected
        ProcessRequest("Job_4", 90),
        ProcessRequest("Job_5", 350),
        ProcessRequest("Job_6", 250),
    ]

    run_workload(
        "3A. Mixed Contention & Oversized (First-Fit)",
        partition_layout,
        mixed_requests,
        "first_fit"
    )
    run_workload(
        "3B. Mixed Contention & Oversized (Best-Fit)",
        partition_layout,
        mixed_requests,
        "best_fit"
    )


if __name__ == "__main__":
    main()
