import secrets


class CapabilitySystem:

    def __init__(self):
        self.capabilities = {}

    def grant(self, user, resource, permissions):

        token = secrets.token_hex(16)

        self.capabilities[token] = {
            "user": user,
            "resource": resource,
            "permissions": set(permissions)
        }

        print(f"Capability granted to {user}")
        print("Resource:", resource)
        print("Permissions:", permissions)
        print("Token:", token)

        return token

    def check_access(self, token, resource, permission):

        capability = self.capabilities.get(token)

        if capability is None:
            print("ACCESS DENIED: Invalid or revoked token")
            return False

        user = capability["user"]

        if (capability["resource"] == resource and
                permission in capability["permissions"]):

            print(f"{user} -> {resource} -> "
                  f"{permission}: ACCESS GRANTED")

            return True

        print(f"{user} -> {resource} -> "
              f"{permission}: ACCESS DENIED")

        return False

    def revoke(self, token):

        if token in self.capabilities:

            user = self.capabilities[token]["user"]

            del self.capabilities[token]

            print(f"Capability revoked for {user}")

        else:
            print("Invalid capability token")

    def display(self):

        print("\n===== ACTIVE CAPABILITIES =====")

        for token, data in self.capabilities.items():

            print("\nUser:", data["user"])
            print("Resource:", data["resource"])
            print("Permissions:",
                  ", ".join(sorted(data["permissions"])))
            print("Token:", token)


if __name__ == "__main__":

    system = CapabilitySystem()

    print("Capability-Based Protection Simulation")
    print("=" * 55)

    # Grant capabilities
    print("\n===== GRANT CAPABILITIES =====")

    admin_token = system.grant(
        "Admin", "File1", ["read", "write", "execute"]
    )

    student_token = system.grant(
        "Student", "File1", ["read", "write"]
    )

    guest_token = system.grant(
        "Guest", "File2", ["read"]
    )

    # Display active capabilities
    system.display()

    # Verify access
    print("\n===== ACCESS VERIFICATION =====")

    system.check_access(admin_token, "File1", "execute")
    system.check_access(student_token, "File1", "write")
    system.check_access(student_token, "File1", "execute")
    system.check_access(guest_token, "File2", "read")
    system.check_access(guest_token, "File2", "write")
    system.check_access(guest_token, "File1", "read")

    # Revoke capability
    print("\n===== REVOKE CAPABILITY =====")

    system.revoke(student_token)

    # Check access after revocation
    print("\n===== ACCESS AFTER REVOCATION =====")

    system.check_access(student_token, "File1", "read")

    # Check invalid token
    system.check_access("invalid_token", "File1", "read")

    # Display remaining capabilities
    system.display()

    print("\nSimulation completed successfully.")
