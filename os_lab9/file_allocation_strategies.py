def contiguous_allocation(start, length):
    blocks = list(range(start, start + length))

    print("\n===== CONTIGUOUS ALLOCATION =====")
    print("Starting Block:", start)
    print("File Length:", length)
    print("Allocated Blocks:", blocks)
    print("Storage Overhead: 0 extra blocks")
    print("Access Method: Direct and Sequential")


def linked_allocation(blocks):
    print("\n===== LINKED ALLOCATION =====")
    print("Starting Block:", blocks[0])
    print("Allocated Blocks:", blocks)

    print("Linked Structure:", end=" ")

    for block in blocks:
        print(block, end=" -> ")

    print("NULL")

    print("Storage Overhead:", len(blocks), "pointers")
    print("Access Method: Sequential")


def indexed_allocation(index_block, blocks):
    print("\n===== INDEXED ALLOCATION =====")
    print("Index Block:", index_block)
    print("Allocated Data Blocks:", blocks)

    print("Index Table:")

    for i, block in enumerate(blocks):
        print(f"Index {i} -> Block {block}")

    print("Storage Overhead: 1 index block")
    print("Access Method: Direct and Sequential")


if __name__ == "__main__":

    print("File Allocation Strategies Simulation")
    print("=" * 55)

    disk_size = 20
    file_size = 5

    print("Total Disk Blocks:", disk_size)
    print("Required Data Blocks:", file_size)

    contiguous_allocation(3, file_size)

    linked_allocation([2, 7, 11, 15, 18])

    indexed_allocation(1, [4, 8, 12, 16, 19])

    print("\n===== PERFORMANCE COMPARISON =====")

    print(f"{'Method':<15}{'Data Blocks':<15}{'Overhead'}")
    print("-" * 50)

    print(f"{'Contiguous':<15}{5:<15}0 extra blocks")
    print(f"{'Linked':<15}{5:<15}5 pointers")
    print(f"{'Indexed':<15}{5:<15}1 index block")

    print("\nSimulation completed successfully.")
