class JournalFileSystem:

    def __init__(self):
        self.disk = {}
        self.journal = []

    def write(self, transaction, filename, content):

        self.journal.append(
            (transaction, "WRITE", filename, content)
        )

        print(f"Transaction {transaction}: "
              f"WRITE {filename} recorded in journal")

    def commit(self, transaction):

        self.journal.append(
            (transaction, "COMMIT", None, None)
        )

        print(f"Transaction {transaction}: COMMITTED")

    def recover(self):

        committed = set()

        for transaction, operation, filename, content in self.journal:

            if operation == "COMMIT":
                committed.add(transaction)

        print("\n===== CRASH RECOVERY =====")

        for transaction, operation, filename, content in self.journal:

            if operation == "WRITE":

                if transaction in committed:

                    self.disk[filename] = content

                    print(f"Transaction {transaction}: "
                          f"Recovered {filename}")

                else:

                    print(f"Transaction {transaction}: "
                          f"Uncommitted operation ignored")

    def display(self):

        print("\nFile-System Contents:")

        if not self.disk:
            print("Disk is empty")

        else:
            for filename, content in self.disk.items():
                print(f"{filename}: {content}")

    def display_journal(self):

        print("\n===== JOURNAL CONTENTS =====")

        for entry in self.journal:
            print(entry)


if __name__ == "__main__":

    fs = JournalFileSystem()

    print("Journaling and Crash Recovery Simulation")
    print("=" * 55)

    # Transaction 1
    fs.write(1, "file1.txt", "Operating Systems")
    fs.commit(1)

    # Transaction 2
    fs.write(2, "file2.txt", "File System Internals")
    fs.commit(2)

    # Transaction 3 - Not committed
    fs.write(3, "file3.txt", "Incomplete Transaction")

    # Display journal
    fs.display_journal()

    # Simulate system crash
    print("\n===== SYSTEM CRASH =====")
    print("System crashed before applying journal to disk")

    fs.display()

    # Recover committed transactions
    fs.recover()

    # Display recovered file system
    fs.display()

    print("\nRecovery completed successfully.")
