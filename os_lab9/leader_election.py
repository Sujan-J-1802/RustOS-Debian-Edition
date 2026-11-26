class BullyElection:

    def __init__(self, total_processes):

        self.processes = {
            pid: True
            for pid in range(1, total_processes + 1)
        }

        self.coordinator = max(self.processes)

    def display(self):

        print("\n===== PROCESS STATUS =====")

        for pid, active in self.processes.items():

            status = "ACTIVE" if active else "FAILED"

            print(f"P{pid}: {status}")

        print("Current Coordinator:", self.coordinator)

    def fail_process(self, pid):

        self.processes[pid] = False

        print(f"\nP{pid} has failed")

        if self.coordinator == pid:

            self.coordinator = None

            print("Coordinator failure detected")

    def election(self, pid):

        if not self.processes[pid]:

            print(f"P{pid} is inactive")
            return

        print(f"\nP{pid} starts election")

        higher_processes = []

        for other_pid in self.processes:

            if other_pid > pid:

                print(f"P{pid} sends ELECTION "
                      f"message to P{other_pid}")

                if self.processes[other_pid]:

                    print(f"P{other_pid} sends OK "
                          f"message to P{pid}")

                    higher_processes.append(other_pid)

                else:

                    print(f"P{other_pid}: No response")

        if higher_processes:

            for higher_pid in higher_processes:

                self.election(higher_pid)

        else:

            self.coordinator = pid

            print(f"\nP{pid} is elected as Coordinator")

            for other_pid, active in self.processes.items():

                if other_pid != pid and active:

                    print(f"P{pid} sends COORDINATOR "
                          f"message to P{other_pid}")

    def recover_process(self, pid):

        self.processes[pid] = True

        print(f"\nP{pid} has recovered")

        self.election(pid)


if __name__ == "__main__":

    print("Bully Leader Election Simulation")
    print("=" * 55)

    # Create five distributed processes
    system = BullyElection(5)

    print("\n===== INITIAL SYSTEM =====")

    system.display()

    # Simulate coordinator failure
    print("\n===== COORDINATOR FAILURE =====")

    system.fail_process(5)

    # Start election from P3
    print("\n===== LEADER ELECTION =====")

    system.election(3)

    system.display()

    # Recover failed process
    print("\n===== PROCESS RECOVERY =====")

    system.recover_process(5)

    # Display final status
    system.display()

    print("\nSimulation completed successfully.")
