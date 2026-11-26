class AccessControl:

    def __init__(self):
        self.matrix = {}

    def add_user(self, username):

        if username not in self.matrix:
            self.matrix[username] = {}
            print("User added:", username)

    def grant(self, username, resource, permissions):

        if username in self.matrix:

            self.matrix[username].setdefault(resource, set())
            self.matrix[username][resource].update(permissions)

            print(f"Permissions granted to {username} "
                  f"for {resource}: {permissions}")

    def revoke(self, username, resource, permission):

        if resource in self.matrix.get(username, {}):

            self.matrix[username][resource].discard(permission)

            print(f"Permission '{permission}' revoked "
                  f"from {username} for {resource}")

    def check_access(self, username, resource, permission):

        permissions = self.matrix.get(
            username, {}
        ).get(resource, set())

        if permission in permissions:
            status = "ACCESS GRANTED"
        else:
            status = "ACCESS DENIED"

        print(f"{username} -> {resource} -> "
              f"{permission}: {status}")

    def display(self):

        resources = sorted({
            resource
            for user in self.matrix.values()
            for resource in user
        })

        print("\n===== ACCESS CONTROL MATRIX =====")

        print(f"{'User':<15}", end="")

        for resource in resources:
            print(f"{resource:<20}", end="")

        print()
        print("-" * (15 + 20 * len(resources)))

        for username, permissions in self.matrix.items():

            print(f"{username:<15}", end="")

            for resource in resources:

                rights = permissions.get(resource, set())
                value = ", ".join(sorted(rights)) or "-"

                print(f"{value:<20}", end="")

            print()


if __name__ == "__main__":

    ac = AccessControl()

    print("Access-Control Simulation")
    print("=" * 55)

    # Add users
    print("\n===== ADD USERS =====")

    ac.add_user("admin")
    ac.add_user("student")
    ac.add_user("guest")

    # Grant permissions
    print("\n===== GRANT PERMISSIONS =====")

    ac.grant("admin", "file1.txt",
             ["read", "write", "execute"])

    ac.grant("admin", "file2.txt",
             ["read", "write"])

    ac.grant("student", "file1.txt",
             ["read", "write"])

    ac.grant("student", "file2.txt",
             ["read"])

    ac.grant("guest", "file1.txt",
             ["read"])

    # Display access control matrix
    ac.display()

    # Check permissions
    print("\n===== ACCESS VERIFICATION =====")

    ac.check_access("admin", "file1.txt", "execute")
    ac.check_access("student", "file1.txt", "write")
    ac.check_access("student", "file2.txt", "write")
    ac.check_access("guest", "file1.txt", "read")
    ac.check_access("guest", "file2.txt", "read")

    # Revoke permission
    print("\n===== REVOKE PERMISSION =====")

    ac.revoke("student", "file1.txt", "write")

    # Verify after revocation
    print("\n===== ACCESS AFTER REVOCATION =====")

    ac.check_access("student", "file1.txt", "write")

    # Display updated matrix
    ac.display()

    print("\nSimulation completed successfully.")
