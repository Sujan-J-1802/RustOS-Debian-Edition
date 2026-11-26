import hashlib
import os
import hmac


class PasswordManager:

    def __init__(self):
        self.users = {}

    def hash_password(self, password, salt):

        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            600000
        )

    def register(self, username, password):

        if username in self.users:
            print("User already exists")
            return

        salt = os.urandom(16)
        password_hash = self.hash_password(password, salt)

        self.users[username] = {
            "salt": salt,
            "hash": password_hash
        }

        print(f"User '{username}' registered successfully")

    def verify(self, username, password):

        if username not in self.users:
            print("User not found")
            return False

        salt = self.users[username]["salt"]
        stored_hash = self.users[username]["hash"]

        entered_hash = self.hash_password(password, salt)

        if hmac.compare_digest(stored_hash, entered_hash):
            print(f"Login successful for '{username}'")
            return True

        print(f"Login failed for '{username}'")
        return False

    def display(self):

        print("\n===== STORED USER CREDENTIALS =====")

        for username, data in self.users.items():

            print("\nUsername:", username)
            print("Salt:", data["salt"].hex())
            print("Password Hash:", data["hash"].hex())


if __name__ == "__main__":

    manager = PasswordManager()

    print("Password Hashing and Verification")
    print("=" * 55)

    # Register users
    print("\n===== USER REGISTRATION =====")

    manager.register("student", "Student@123")
    manager.register("admin", "Admin@456")

    # Display stored credentials
    manager.display()

    # Verify passwords
    print("\n===== PASSWORD VERIFICATION =====")

    manager.verify("student", "Student@123")
    manager.verify("student", "WrongPassword")
    manager.verify("admin", "Admin@456")
    manager.verify("guest", "Guest@123")

    print("\nSimulation completed successfully.")
