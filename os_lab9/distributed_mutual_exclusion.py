class Process:

    def __init__(self, pid):

        self.pid = pid
        self.clock = 0
        self.state = "RELEASED"
        self.request_time = None
        self.replies = set()
        self.deferred = []

    def request_cs(self, processes):

        self.clock += 1
        self.request_time = self.clock
        self.state = "WANTED"
        self.replies.clear()

        print(f"\nP{self.pid} requests critical section")
        print("Request timestamp:", self.request_time)

        for process in processes:

            if process.pid != self.pid:

                print(f"P{self.pid} sends REQUEST "
                      f"to P{process.pid}")

                process.receive_request(
                    self, self.request_time
                )

    def receive_request(self, sender, timestamp):

        self.clock = max(self.clock, timestamp) + 1

        defer = (
            self.state == "HELD" or
            (
                self.state == "WANTED" and
                (self.request_time, self.pid) <
                (timestamp, sender.pid)
            )
        )

        if defer:

            self.deferred.append(sender)

            print(f"P{self.pid} defers REPLY "
                  f"to P{sender.pid}")

        else:

            self.send_reply(sender)

    def send_reply(self, receiver):

        self.clock += 1

        print(f"P{self.pid} sends REPLY "
              f"to P{receiver.pid}")

        receiver.receive_reply(self.pid, self.clock)

    def receive_reply(self, sender_pid, timestamp):

        self.clock = max(self.clock, timestamp) + 1

        self.replies.add(sender_pid)

    def enter_cs(self, total_processes):

        if (self.state == "WANTED" and
                len(self.replies) == total_processes - 1):

            self.state = "HELD"

            print(f"\nP{self.pid} ENTERS critical section")

            return True

        print(f"\nP{self.pid} is waiting for REPLY messages")

        return False

    def release_cs(self):

        if self.state != "HELD":
            return

        self.state = "RELEASED"
        self.clock += 1
        self.request_time = None

        print(f"\nP{self.pid} EXITS critical section")

        for process in self.deferred:

            self.send_reply(process)

        self.deferred.clear()

    def display(self):

        print(f"P{self.pid}: "
              f"State = {self.state}, "
              f"Clock = {self.clock}")


if __name__ == "__main__":

    print("Distributed Mutual Exclusion Simulation")
    print("=" * 55)

    # Create distributed processes
    p1 = Process(1)
    p2 = Process(2)
    p3 = Process(3)

    processes = [p1, p2, p3]
    total = len(processes)

    print("\n===== INITIAL PROCESS STATES =====")

    for process in processes:
        process.display()

    print("\n===== CRITICAL SECTION REQUESTS =====")

    # P1 requests and enters critical section
    p1.request_cs(processes)
    p1.enter_cs(total)

    # P2 requests while P1 holds critical section
    p2.request_cs(processes)
    p2.enter_cs(total)

    # P3 requests critical section
    p3.request_cs(processes)
    p3.enter_cs(total)

    print("\n===== CRITICAL SECTION RELEASE =====")

    # P1 releases critical section
    p1.release_cs()

    # P2 enters and releases critical section
    if p2.enter_cs(total):
        p2.release_cs()

    # P3 enters and releases critical section
    if p3.enter_cs(total):
        p3.release_cs()

    print("\n===== FINAL PROCESS STATES =====")

    for process in processes:
        process.display()

    print("\nSimulation completed successfully.")
