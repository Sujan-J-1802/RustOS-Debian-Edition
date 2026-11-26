class FileSystem:

    def __init__(self):
        self.root = {}

    def lookup(self, path):
        parts = path.strip("/").split("/")
        current = self.root

        if path == "/":
            return current

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None

        return current

    def mkdir(self, path):
        parts = path.strip("/").split("/")
        current = self.root

        for part in parts:
            if part not in current:
                current[part] = {}

            if not isinstance(current[part], dict):
                print("Invalid directory path:", path)
                return

            current = current[part]

        print("Directory created:", path)

    def create_file(self, path, content):
        parent, name = path.rsplit("/", 1)
        directory = self.lookup(parent or "/")

        if isinstance(directory, dict) and name not in directory:
            directory[name] = content
            print("File created:", path)
        else:
            print("Cannot create file:", path)

    def delete(self, path):
        parent, name = path.rsplit("/", 1)
        directory = self.lookup(parent or "/")

        if isinstance(directory, dict) and name in directory:
            del directory[name]
            print("Deleted:", path)
        else:
            print("Path not found:", path)

    def traverse(self, directory=None, level=0):

        if directory is None:
            directory = self.root
            print("/")

        for name, value in directory.items():

            if isinstance(value, dict):
                print("    " * level + "|-- " + name + "/")
                self.traverse(value, level + 1)

            else:
                print("    " * level + "|-- " + name)


if __name__ == "__main__":

    fs = FileSystem()

    print("Hierarchical Directory Structure Simulation")
    print("=" * 55)

    # Create directories
    fs.mkdir("/home")
    fs.mkdir("/home/student")
    fs.mkdir("/home/student/documents")
    fs.mkdir("/home/student/downloads")
    fs.mkdir("/etc")

    # Create files
    fs.create_file(
        "/home/student/documents/notes.txt",
        "Operating Systems Notes"
    )

    fs.create_file(
        "/home/student/downloads/program.py",
        "print('Hello World')"
    )

    fs.create_file(
        "/etc/config.txt",
        "System Configuration"
    )

    # Display directory structure
    print("\nInitial Directory Structure:")
    fs.traverse()

    # Search for a file
    path = "/home/student/documents/notes.txt"

    print("\nPath Lookup:", path)

    result = fs.lookup(path)

    if result is not None:
        print("File found")
        print("Content:", result)
    else:
        print("File not found")

    # Delete a file
    print()
    fs.delete("/home/student/downloads/program.py")

    # Delete a directory
    fs.delete("/home/student/downloads")

    # Display updated structure
    print("\nUpdated Directory Structure:")
    fs.traverse()

    print("\nSimulation completed successfully.")
