class Hypervisor:

    def __init__(self, cpu, memory, io):

        self.total = {
            "CPU": cpu,
            "Memory": memory,
            "IO": io
        }

        self.available = self.total.copy()
        self.vms = {}

    def allocate(self, name, cpu, memory, io):

        request = {
            "CPU": cpu,
            "Memory": memory,
            "IO": io
        }

        if name in self.vms:
            print(f"{name} already exists")
            return False

        for resource, amount in request.items():

            if amount > self.available[resource]:
                print(f"{name}: Allocation failed")
                print(f"Insufficient {resource} resources")
                return False

        for resource, amount in request.items():

            self.available[resource] -= amount

        self.vms[name] = request

        print(f"{name}: Resources allocated successfully")

        return True

    def release(self, name):

        if name not in self.vms:
            print("Virtual machine not found")
            return

        for resource, amount in self.vms[name].items():

            self.available[resource] += amount

        del self.vms[name]

        print(f"{name}: Resources released successfully")

    def display(self):

        print("\n===== VIRTUAL MACHINE ALLOCATION =====")

        print(f"{'VM':<10}{'CPU':<10}"
              f"{'RAM (GB)':<15}{'IO (MB/s)':<15}")

        print("-" * 50)

        for name, resources in self.vms.items():

            print(f"{name:<10}"
                  f"{resources['CPU']:<10}"
                  f"{resources['Memory']:<15}"
                  f"{resources['IO']:<15}")

        print("\n===== HOST RESOURCE STATUS =====")

        for resource in self.total:

            total = self.total[resource]
            available = self.available[resource]
            used = total - available

            utilization = (used / total) * 100

            print(f"{resource}:")
            print("  Total:", total)
            print("  Used:", used)
            print("  Available:", available)
            print(f"  Utilization: {utilization:.2f}%")


if __name__ == "__main__":

    print("Virtual Machine Resource Allocation")
    print("=" * 55)

    # Initialize host resources
    hypervisor = Hypervisor(
        cpu=8,
        memory=16,
        io=1000
    )

    # Allocate resources
    print("\n===== RESOURCE ALLOCATION =====")

    hypervisor.allocate("VM1", 2, 4, 200)
    hypervisor.allocate("VM2", 3, 6, 300)
    hypervisor.allocate("VM3", 2, 4, 400)

    # Request exceeding available resources
    hypervisor.allocate("VM4", 2, 4, 200)

    # Display resource utilization
    hypervisor.display()

    # Release resources
    print("\n===== RESOURCE RELEASE =====")

    hypervisor.release("VM2")

    # Retry allocation
    print("\n===== RESOURCE REALLOCATION =====")

    hypervisor.allocate("VM4", 2, 4, 200)

    # Display final resource status
    hypervisor.display()

    print("\nSimulation completed successfully.")
