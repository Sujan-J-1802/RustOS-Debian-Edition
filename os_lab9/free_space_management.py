class FreeSpaceManagement:

    def __init__(self, total_blocks):
        self.total_blocks = total_blocks
        self.bitmap = [0] * total_blocks
        self.free_list = list(range(total_blocks))

    def allocate(self, count):

        if count > len(self.free_list):
            print("Insufficient free space")
            return []

        allocated = self.free_list[:count]

        for block in allocated:
            self.bitmap[block] = 1
            self.free_list.remove(block)

        print("Allocated Blocks:", allocated)

        return allocated

    def deallocate(self, blocks):

        for block in blocks:
            if 0 <= block < self.total_blocks:
                if self.bitmap[block] == 1:
                    self.bitmap[block] = 0
                    self.free_list.append(block)

        self.free_list.sort()

        print("Released Blocks:", blocks)

    def display(self):

        print("Bitmap:", self.bitmap)
        print("Free List:", self.free_list)
        print("Total Blocks:", self.total_blocks)
        print("Allocated Blocks:", sum(self.bitmap))
        print("Free Blocks:", len(self.free_list))

        utilization = sum(self.bitmap) / self.total_blocks * 100

        print(f"Disk Utilization: {utilization:.2f}%")


if __name__ == "__main__":

    disk = FreeSpaceManagement(20)

    print("Free-Space Management Simulation")
    print("=" * 60)

    print("\n1. Initial Disk Status")
    disk.display()

    print("\n2. Allocate 5 Blocks")
    disk.allocate(5)
    disk.display()

    print("\n3. Allocate 4 More Blocks")
    disk.allocate(4)
    disk.display()

    print("\n4. Release Blocks 1, 3 and 6")
    disk.deallocate([1, 3, 6])
    disk.display()

    print("\n5. Allocate 3 Blocks")
    disk.allocate(3)
    disk.display()

    print("\nSimulation completed successfully.")
