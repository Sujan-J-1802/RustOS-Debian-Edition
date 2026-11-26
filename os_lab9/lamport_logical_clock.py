class Process:

    def __init__(self, name):

        self.name = name
        self.clock = 0

    def internal_event(self):

        self.clock += 1

        print(f"{self.name}: Internal event")
        print(f"Logical Clock: {self.clock}")

    def send_message(self, receiver):

        self.clock += 1

        timestamp = self.clock

        print(f"\n{self.name} sends message to {receiver.name}")
        print(f"Send Timestamp: {timestamp}")

        receiver.receive_message(self.name, timestamp)

    def receive_message(self, sender, timestamp):

        old_clock = self.clock

        self.clock = max(self.clock, timestamp) + 1

        print(f"{self.name} receives message from {sender}")
        print(f"Previous Clock: {old_clock}")
        print(f"Received Timestamp: {timestamp}")
        print(f"Updated Clock: {self.clock}")

    def display(self):

        print(f"{self.name}: Logical Clock = {self.clock}")


if __name__ == "__main__":

    print("Lamport Logical Clock Simulation")
    print("=" * 55)

    # Create distributed processes
    p1 = Process("P1")
    p2 = Process("P2")
    p3 = Process("P3")

    print("\n===== INITIAL CLOCK VALUES =====")

    p1.display()
    p2.display()
    p3.display()

    # Internal events
    print("\n===== INTERNAL EVENTS =====")

    p1.internal_event()
    p2.internal_event()
    p3.internal_event()

    # Message passing
    print("\n===== MESSAGE PASSING =====")

    p1.send_message(p2)

    p2.internal_event()

    p2.send_message(p3)

    p3.internal_event()

    p3.send_message(p1)

    # Final clock values
    print("\n===== FINAL LOGICAL CLOCKS =====")

    p1.display()
    p2.display()
    p3.display()

    print("\nSimulation completed successfully.")
