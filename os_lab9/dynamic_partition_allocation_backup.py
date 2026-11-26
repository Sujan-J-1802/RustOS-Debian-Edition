"""
Recommended OS lab: Dynamic Partition Memory Allocation.
This is a pedagogical simulation/user-space demonstration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Strategy = Literal["first_fit", "best_fit", "worst_fit"]


@dataclass
class MemoryBlock:
    start_kb: int
    size_kb: int
    pid: str | None = None  # None indicates a free hole

    @property
    def end_kb(self) -> int:
        return self.start_kb + self.size_kb

    @property
    def is_free(self) -> bool:
        return self.pid is None


@dataclass
class Event:
    action: Literal["alloc", "free"]
    pid: str
    size_kb: int = 0


class DynamicMemoryAllocator:
    """Simulates variable-size contiguous memory allocation (NT) with coalescing."""

    def __init__(
        self,
        total_memory_kb: int,
        strategy: Strategy = "first_fit"
    ) -> None:
        self.total_memory_kb = total_memory_kb
        self.strategy = strategy
        self.blocks: list[MemoryBlock] = [
            MemoryBlock(0, total_memory_kb)
        ]
        self.rejected: list[tuple[str, int, str]] = []

    @property
    def total_allocated_kb(self) -> int:
        return sum(
            b.size_kb for b in self.blocks if not b.is_free
        )

    @property
    def total_free_kb(self) -> int:
        return sum(
            b.size_kb for b in self.blocks if b.is_free
        )

    @property
    def free_hole_count(self) -> int:
        return sum(1 for b in self.blocks if b.is_free)

    @property
    def largest_free_hole_kb(self) -> int:
        return max(
            (b.size_kb for b in self.blocks if b.is_free),
            default=0
        )

    @property
    def external_fragmentation_pct(self) -> float:
        """
        (largest_free_block / total_free_memory) when free memory exists.
        """
        free_total = self.total_free_kb
        if free_total == 0:
            return 0.0

        return (
            1.0 - self.largest_free_hole_kb / free_total
        ) * 100

    def allocate(self, pid: str, size_kb: int) -> bool:
        candidates = [
            (idx, blk)
            for idx, blk in enumerate(self.blocks)
            if blk.is_free and blk.size_kb >= size_kb
        ]

        if not candidates:
            reason = (
                f"External fragmentation (Total free={self.total_free_kb} KB), "
                f"Max contiguous hole={self.largest_free_hole_kb} KB"
                if self.total_free_kb >= size_kb
                else f"Insufficient total memory ({self.total_free_kb} KB < {size_kb} KB)"
            )
            self.rejected.append((pid, size_kb, reason))
            return False

        if self.strategy == "best_fit":
            chosen_idx, chosen_blk = min(
                candidates, key=lambda item: (item[1].size_kb - size_kb)
            )
        elif self.strategy == "worst_fit":
            chosen_idx, chosen_blk = max(
                candidates, key=lambda item: (item[1].size_kb - size_kb)
            )
        else:
            chosen_idx, chosen_blk = candidates[0]

        # Allocate exact requested size; split remaining space into a smaller hole if > 0
        allocated_block = MemoryBlock(
            start_kb=chosen_blk.start_kb,
            size_kb=size_kb,
            pid=pid
        )

        remainder_size = chosen_blk.size_kb - size_kb

        if remainder_size > 0:
            remainder_block = MemoryBlock(
                start_kb=chosen_blk.start_kb + size_kb,
                size_kb=remainder_size,
                pid=None
            )
            self.blocks[chosen_idx:chosen_idx + 1] = [
                allocated_block,
                remainder_block
            ]
        else:
            self.blocks[chosen_idx] = allocated_block

        return True

    def deallocate(self, pid: str) -> bool:
        freed = False

        for blk in self.blocks:
            if blk.pid == pid:
                blk.pid = None
                freed = True

        if freed:
            self.coalesce()

        return freed

    def coalesce(self) -> None:
        """Merge adjacent free holes into a single contiguous block."""
        merged: list[MemoryBlock] = []

        for blk in self.blocks:
            if merged and merged[-1].is_free and blk.is_free:
                merged[-1].size_kb += blk.size_kb
            else:
                merged.append(blk)

        self.blocks = merged

    def compact(self) -> None:
        """Relocate all allocated blocks to the start of RAM, merging all free holes."""
        allocated = [b for b in self.blocks if not b.is_free]

        cursor = 0
        compacted: list[MemoryBlock] = []

        for blk in allocated:
            compacted.append(
                MemoryBlock(
                    start_kb=cursor,
                    size_kb=blk.size_kb,
                    pid=blk.pid
                )
            )
            cursor += blk.size_kb

        if cursor < self.total_memory_kb:
            compacted.append(
                MemoryBlock(
                    start_kb=cursor,
                    size_kb=self.total_memory_kb - cursor,
                    pid=None
                )
            )

        self.blocks = compacted

    def print_report(self, scenario_name: str) -> None:
        print("\n" + "=" * 74)
        print(f"Scenario : {scenario_name}")
        print(f"Strategy : {self.strategy.upper()} | Total RAM: {self.total_memory_kb} KB")
        print("-" * 74)
        print(
            f"{'Range (KB)':<16} | {'Size (KB)':<10} | "
            f"{'Status':<10} | {'Process':<10}"
        )
        print("-" * 74)

        for b in self.blocks:
            rng = f"{b.start_kb}-{b.end_kb}"
            status = "FREE" if b.is_free else "ALLOCATED"
            proc = "-" if b.is_free else b.pid

            print(
                f"{rng:<16} | {b.size_kb:<10} | "
                f"{status:<10} | {proc:<10}"
            )

        print("-" * 74)
print("Before Compaction -> Attempting to allocate P8 (220 KB)")
p8_before = compaction_sim.allocate("P8", 220)
print(f"Allocation succeeded (before): {p8_before}. Total free: {compaction_sim.total_free_kb} KB, Largest hole: {compaction_sim.largest_free_hole_kb} KB")

compaction_sim.compact()

print("After Compaction -> Attempting to allocate P8 (220 KB)")
p8_after = compaction_sim.allocate("P8", 220)
print(f"Allocation succeeded (after): {p8_after}")
compaction_sim.print_report("5. Post-Compaction Memory Layout")


if __name__ == "__main__":
    main()        print(
            f"Metrics: Allocated = {self.total_allocated_kb} KB | "
            f"Total Free = {self.total_free_kb} KB across "
            f"{self.free_hole_count} hole(s) | "
            f"Largest Hole = {self.largest_free_hole_kb} KB"
        )

        print(
            f"Fragmentation: External Fragmentation Index = "
            f"{self.external_fragmentation_pct:.1f}%"
        )

        print("Internal Fragmentation: 0 KB")

        if self.rejected:
            print("Rejected:")

            for pid, s, reason in self.rejected:
                print(f"  - {pid} ({s} KB): {reason}")


def run_scenario(
    title: str,
    total_ram: int,
    events: list[Event],
    strategies: list[Strategy]
) -> None:
    for strat in strategies:
        sim = DynamicMemoryAllocator(total_ram, strategy=strat)

        for ev in events:
            if ev.action == "alloc":
                sim.allocate(ev.pid, ev.size_kb)
            elif ev.action == "free":
                sim.deallocate(ev.pid)

        sim.print_report(title)


def main() -> None:
    print("Dynamic Partition Memory Allocation")
    print("=" * 70)
    print("\t\t(Dynamic Partition Memory Allocation)")

    # Scenario 1: Classic checkerboard fragmentation across First-Fit, Best-Fit, Worst-Fit
    checkerboard_events = [
        Event("alloc", "P1", 200),
        Event("alloc", "P2", 150),
        Event("alloc", "P3", 250),
        Event("alloc", "P4", 100),
        Event("alloc", "P5", 200),

        # Free non-adjacent blocks P2 (150 KB) and P4 (100 KB); total hole is 250 KB
        Event("free", "P2"),
        Event("free", "P4"),

        # Allocate P6 (90 KB) and P7 (140 KB) to observe hole placement differences
        Event("alloc", "P6", 90),
        Event("alloc", "P7", 140),

        # Request P8 (220 KB): total free is 220 KB, but split across holes!
        Event("alloc", "P8", 220),
    ]

    run_scenario(
        "1. Checkerboard Allocation & External Fragmentation",
        total_ram=1000,
        events=checkerboard_events,
        strategies=["first_fit", "best_fit", "worst_fit"],
    )

    # Scenario 2: Adjacent deallocation demonstrating automatic hole coalescing
    coalesce_events = [
        Event("alloc", "A", 300),
        Event("alloc", "B", 200),
        Event("alloc", "C", 300),
        Event("free", "A"),
        Event("free", "B"),  # Coalesces A (300) + B (200) into a single 500 KB hole
        Event("alloc", "D", 450),  # Succeeds because A and B are merged
    ]

    run_scenario(
        "2. Adjacent Deallocation & Hole Coalescing",
        total_ram=1000,
        events=coalesce_events,
        strategies=["first_fit"],
    )

    # Scenario 3: Memory Compaction resolving external fragmentation failure
    print("\n" + "=" * 70)
    print("Scenario 3: Compaction Resolving External Fragmentation (First-Fit)")
    print("=" * 70)

    compaction_sim = DynamicMemoryAllocator(1000, strategy="first_fit")

    for ev in checkerboard_events:
        if ev.action == "alloc":
            compaction_sim.allocate(ev.pid, ev.size_kb)
        else:
            compaction_sim.deallocate(ev.pid)
print("Before Compaction -> Attempting to allocate P8 (220 KB)")
p8_before = compaction_sim.allocate("P8", 220)
print(f"Allocation succeeded (before): {p8_before}. Total free: {compaction_sim.total_free_kb} KB, Largest hole: {compaction_sim.largest_free_hole_kb} KB")

compaction_sim.compact()

print("After Compaction -> Attempting to allocate P8 (220 KB)")
p8_after = compaction_sim.allocate("P8", 220)
print(f"Allocation succeeded (after): {p8_after}")
compaction_sim.print_report("5. Post-Compaction Memory Layout")


if __name__ == "__main__":
    main()
