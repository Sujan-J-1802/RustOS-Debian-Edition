"""Recommended OS: Paging and Address Translation.
This is a pedagogical simulation/user-space demonstration."""

from __future__ import annotations
from collections import OrderedDict
from dataclasses import dataclass
import time


@dataclass
class PageTableEntry:
    frame_number: int | None
    valid: bool
    read_only: bool = False


@dataclass
class TranslationResult:
    logical_addr: int
    page_num: int
    offset: int
    frame_num: int | None
    physical_addr: int | None
    tlb_hit: bool
    status: str
    latency_ns: int


class MemoryManagementUnit:
    """Simulates logical-to-physical address translation using a TLB and Page Table."""

    def __init__(
        self,
        page_size_bytes: int,
        num_logical_pages: int,
        num_physical_frames: int,
        tlb_capacity: int = 4,
    ) -> None:

        if (page_size_bytes & (page_size_bytes - 1)) != 0:
            raise ValueError("Page size must be a power of 2.")

        self.page_size = page_size_bytes
        self.offset_bits = page_size_bytes.bit_length() - 1
        self.offset_mask = page_size_bytes - 1
        self.num_pages = num_logical_pages
        self.num_frames = num_physical_frames
        self.max_logical_addr = (num_logical_pages * page_size_bytes) - 1

        # Page table initialized with all entries invalid
        self.page_table: dict[int, PageTableEntry] = {
            p: PageTableEntry(frame_number=None, valid=False)
            for p in range(num_logical_pages)
        }

        # LRU TLB cache: page_num -> frame_num
        self.tlb_capacity = tlb_capacity
        self.tlb: OrderedDict[int, int] = OrderedDict()

        # Metrics
        self.tlb_hits = 0
        self.tlb_misses = 0
        self.page_faults = 0
        self.protection_faults = 0

    def map_page(self, page_num: int, frame_num: int, read_only: bool = False) -> None:
        if not (0 <= page_num < self.num_pages):
            raise ValueError(f"Invalid page number: {page_num}")
        if not (0 <= frame_num < self.num_frames):
            raise ValueError(f"Invalid frame number: {frame_num}")

        self.page_table[page_num] = PageTableEntry(
            frame_number=frame_num, valid=True, read_only=read_only
        )

    def _lookup_tlb(self, page_num: int) -> int | None:
        if page_num in self.tlb:
            self.tlb.move_to_end(page_num)
            return self.tlb[page_num]
        return None

    def _update_tlb(self, page_num: int, frame_num: int) -> None:
        if page_num in self.tlb:
            self.tlb.move_to_end(page_num)
        else:
            if len(self.tlb) >= self.tlb_capacity:
                self.tlb.popitem(last=False)
        self.tlb[page_num] = frame_num

    def translate(self, logical_addr: int, is_write: bool = False) -> TranslationResult:
        t0 = time.perf_counter_ns()

        # 1. Bounds check against logical address space
        if logical_addr < 0 or logical_addr > self.max_logical_addr:
            elapsed = time.perf_counter_ns() - t0
            return TranslationResult(
                logical_addr,
                logical_addr >> self.offset_bits,
                logical_addr & self.offset_mask,
                None,
                None,
                False,
                "SEGMENTATION FAULT (Out of Logical Bounds)",
                elapsed,
            )

        # 2. Bitwise decomposition: p = addr >> o, d = addr & (2^o - 1)
        page_num = logical_addr >> self.offset_bits
        offset = logical_addr & self.offset_mask

        # 3. Check TLB first
        cached_frame = self._lookup_tlb(page_num)
        if cached_frame is not None:
            pte = self.page_table[page_num]

            if is_write and pte.read_only:
                self.protection_faults += 1
                elapsed = time.perf_counter_ns() - t0
                return TranslationResult(
                    logical_addr, page_num, offset, cached_frame, None, True,
                    "PROTECTION FAULT (Write to Read-Only Page)", elapsed
                )

            self.tlb_hits += 1
            phys_addr = (cached_frame << self.offset_bits) | offset
            elapsed = time.perf_counter_ns() - t0
            return TranslationResult(
                logical_addr, page_num, offset, cached_frame, phys_addr, True,
                "OK (TLB HIT)", elapsed
            )

        # 4. TLB Miss -> Walk Page Table
        self.tlb_misses += 1
        pte = self.page_table[page_num]

        if not pte.valid or pte.frame_number is None:
            self.page_faults += 1
            elapsed = time.perf_counter_ns() - t0
            return TranslationResult(
                logical_addr, page_num, offset, None, None, False,
                "PAGE FAULT (Invalid/Unmapped Page)", elapsed
            )

        if is_write and pte.read_only:
            self.protection_faults += 1
            elapsed = time.perf_counter_ns() - t0
            return TranslationResult(
                logical_addr, page_num, offset, pte.frame_number, None, False,
                "PROTECTION FAULT (Write to Read-Only Page)", elapsed
            )

        # 5. Update TLB and compute physical address: (frame * page_size) + offset
        self._update_tlb(page_num, pte.frame_number)

        phys_addr = (pte.frame_number << self.offset_bits) | offset
        elapsed = time.perf_counter_ns() - t0

        return TranslationResult(
            logical_addr, page_num, offset, pte.frame_number, phys_addr, False,
            "OK (Page Table Walk)", elapsed
        )

    def print_page_table(self) -> None:
        print(f"Page Table Configuration (Page Size = {self.page_size} B, Offset Bits = {self.offset_bits}):")
        print("Page # | Frame # | Valid? | Permissions")
        print("-" * 44)

        for p, entry in self.page_table.items():
            frame_str = str(entry.frame_number) if entry.frame_number is not None else "-"
            valid_str = "V" if entry.valid else "I"
            perm_str = "Read-Only" if entry.read_only else "Read/Write"
            print(f"{p:6} | {frame_str:7} | {valid_str:6} | {perm_str:12}")


def main() -> None:
    print("Paging and Address Translation")
    print("=" * len("Paging and Address Translation"))

    # 16-bit logical address space with 4 KB (4096-byte) pages -> 16 logical pages, 32 physical frames
    mmu = MemoryManagementUnit(
        page_size_bytes=4096,
        num_logical_pages=16,
        num_physical_frames=32,
        tlb_capacity=3,
    )

    # Map subset of pages to non-contiguous physical frames
    mmu.map_page(0, frame_num=5, read_only=False)   # Code segment (.text)
    mmu.map_page(1, frame_num=9, read_only=True)    # Data segment (.data)
    mmu.map_page(2, frame_num=12, read_only=False)  # Heap
    mmu.map_page(7, frame_num=2, read_only=False)   # Shared buffer
    mmu.map_page(15, frame_num=27, read_only=False) # Stack

    mmu.print_page_table()

    # Workload trace testing normal translations, TLB hits, protection faults, page faults, and out-of-bounds
    access_trace: list[tuple[int, bool, str]] = [
        (0x0024, False, "Instruction fetch in Page 0"),
        (0x0100, False, "Second fetch in Page 0 (TLB Hit)"),
        (0x0100, True, "Illegal write to Read-Only Page 1"),
        (0x1400, True, "Write variable in Page 1"),
        (0x2010, False, "Heap read in Page 2"),
        (0x7FFF, True, "Stack access in Page 7"),
        (0x3200, False, "Unmapped Page 3 access (Page Fault)"),
        (0xF800, True, "Stack push in Page 15 (evicts old TLB entry)"),
        (0x0050, False, "Re-access Page 0 after TLB eviction"),
        (0x12000, False, "Address beyond 64 KB logical space"),
    ]

    print("\nMemory Access Translation Trace:")
    print("=" * 100)
    print(
        f"{'Logical':<9} | {'Page':<5} | {'Offset':<7} | {'Frame':<6} | "
        f"{'Physical':<10} | {'Status':<36} | {'Note'}"
    )
    print("-" * 100)

    for addr, is_write, note in access_trace:
        res = mmu.translate(addr, is_write=is_write)

        log_hex = f"0x{res.logical_addr:04X}"
        off_hex = f"0x{res.offset:03X}"
        frm_str = str(res.frame_num) if res.frame_num is not None else "-"
        phy_hex = f"0x{res.physical_addr:05X}" if res.physical_addr is not None else "-"

        print(
            f"{log_hex:<9} | {res.page_num:<5} | {off_hex:<7} | {frm_str:<6} | "
            f"{phy_hex:<10} | {res.status:<36} | {note}"
        )

    total_lookups = mmu.tlb_hits + mmu.tlb_misses
    hit_rate = (mmu.tlb_hits / total_lookups * 100) if total_lookups else 0.0

    print("-" * 108)
    print(
        f"Summary Metrics: TLB Hits = {mmu.tlb_hits}/{total_lookups} ({hit_rate:.1f}%) | "
        f"Page Faults = {mmu.page_faults} | Protection Faults = {mmu.protection_faults}"
    )


if __name__ == "__main__":
    main()
