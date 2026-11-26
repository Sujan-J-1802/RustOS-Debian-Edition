class ProtectionSystem:

    def __init__(self):
        self.matrix = {
            "Admin": {
                "File1": {"R", "W", "X"},
                "File2": {"R", "W"},
                "Printer": {"X"}
            },
            "Student": {
                "File1": {"R", "W"},
                "File2": {"R"},
                "Printer": {"X"}
            },
            "Guest": {
                "File1": {"R"},
                "File2": set(),
                "Printer": set()
            }
        }

    def display_matrix(self):

        print("\n===== PROTECTION ACCESS MATRIX =====")

        resources = ["File1", "File2", "Printer"]

        print(f"{'User':<15}", end="")

        for resource in resources:
            print(f"{resource:<15}", end="")

        print()
        print("-" * 60)

        for user, permissions in self.matrix.items():

            print(f"{user:<15}", end="")

            for resource in resources:

                rights = permissions.get(resource, set())
                value = ", ".join(sorted(rights)) or "-"

                print(f"{value:<15}", end="")

            print()

    def display_acl(self):

        print("\n===== ACCESS CONTROL LISTS =====")

        resources = ["File1", "File2", "Printer"]

        for resource in resources:

            print(f"\nResource: {resource}")

            for user, permissions in self.matrix.items():

                rights = permissions.get(resource, set())

                if rights:
                    print(f"  {user}: "
                          f"{', '.join(sorted(rights))}")

    def display_capabilities(self):

        print("\n===== CAPABILITY LISTS =====")

        for user, permissions in self.matrix.items():

            print(f"\nUser: {user}")

            for resource, rights in permissions.items():

                if rights:
                    print(f"  {resource}: "
                          f"{', '.join(sorted(rights))}")

    def check_access(self, user, resource, permission):

        rights = self.matrix.get(
            user, {}
        ).get(resource, set())

        if permission in rights:
            status = "ACCESS GRANTED"
        else:
            status = "ACCESS DENIED"

        print(f"{user} -> {resource} -> "
              f"{permission}: {status}")


if __name__ == "__main__":

    system = ProtectionSystem()

    print("Protection Access Matrix Simulation")
    print("=" * 60)

    # Display access matrix
    system.display_matrix()

    # Generate access-control lists
    system.display_acl()

    # Generate capability lists
    system.display_capabilities()

    # Verify access permissions
    print("\n===== ACCESS VERIFICATION =====")

    system.check_access("Admin", "File1", "X")
    system.check_access("Student", "File1", "W")
    system.check_access("Student", "File2", "W")
    system.check_access("Guest", "File1", "R")
    system.check_access("Guest", "Printer", "X")

    print("\nSimulation completed successfully.")
