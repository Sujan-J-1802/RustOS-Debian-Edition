import os
import shutil
import stat
from pathlib import Path
from datetime import datetime


def create_directory(directory):

    directory.mkdir(parents=True, exist_ok=True)

    print("Directory created:", directory)


def create_file(file_path):

    with open(file_path, "w") as file:

        file.write("Windows File-System API Demonstration\n")
        file.write("Operating Systems Laboratory\n")

    print("File created:", file_path.name)


def read_file(file_path):

    print("\n===== FILE CONTENT =====")

    with open(file_path, "r") as file:

        print(file.read())


def file_information(file_path):

    information = file_path.stat()

    print("\n===== FILE INFORMATION =====")

    print("File Name:", file_path.name)
    print("Absolute Path:", file_path.resolve())
    print("File Extension:", file_path.suffix)
    print("File Size:", information.st_size, "bytes")

    print(
        "Last Modified:",
        datetime.fromtimestamp(information.st_mtime)
    )

    print("Is File:", file_path.is_file())
    print("Is Directory:", file_path.is_dir())


def copy_file(source, destination):

    shutil.copy2(source, destination)

    print("\nFile copied:", destination.name)


def rename_file(source, destination):

    source.rename(destination)

    print("File renamed:", destination.name)


def check_case_sensitivity(file_path):

    uppercase_path = file_path.with_name(
        file_path.name.upper()
    )

    print("\n===== CASE SENSITIVITY TEST =====")

    print("Original Name:", file_path.name)
    print("Uppercase Name:", uppercase_path.name)

    if uppercase_path.exists():

        print("Uppercase path exists")

        if file_path.samefile(uppercase_path):

            print("Both names refer to the same file")
            print("Case-insensitive behavior detected")

        else:

            print("Both names refer to different files")

    else:

        print("Case-sensitive behavior detected")


def check_permissions(file_path):

    print("\n===== FILE PERMISSIONS =====")

    original_mode = file_path.stat().st_mode

    print("Initially Writable:",
          os.access(file_path, os.W_OK))

    try:

        # Set read-only attribute
        file_path.chmod(stat.S_IREAD)

        print("Read-only attribute applied")

        print("Writable After Change:",
              os.access(file_path, os.W_OK))

    finally:

        # Restore original permissions
        file_path.chmod(original_mode)

    print("Original permissions restored")


def disk_information(directory):

    total, used, free = shutil.disk_usage(directory)

    gb = 1024 ** 3

    print("\n===== DISK INFORMATION =====")

    print(f"Total Space: {total / gb:.2f} GB")
    print(f"Used Space: {used / gb:.2f} GB")
    print(f"Free Space: {free / gb:.2f} GB")


def display_directory(directory):

    print("\n===== DIRECTORY CONTENTS =====")

    for item in sorted(directory.iterdir()):

        item_type = "Directory" if item.is_dir() else "File"

        print(f"{item.name:<25} {item_type}")


if __name__ == "__main__":

    print("Windows File-System API Demonstration")
    print("=" * 60)

    if os.name != "nt":

        print("Error: Run this program on Windows")
        raise SystemExit(1)

    print("Operating System:", os.name)
    print("Path Separator:", os.sep)
    print("Current Directory:", os.getcwd())

    # Create a new laboratory directory
    directory = Path("windows_fs_lab")

    # Avoid modifying an existing directory
    if directory.exists():

        print("Lab directory already exists.")
        print("Rename it before running this program.")
        raise SystemExit(1)

    create_directory(directory)

    original = directory / "sample.txt"
    copied = directory / "copy.txt"
    renamed = directory / "renamed.txt"

    # Create and read file
    create_file(original)
    read_file(original)

    # Display file metadata
    file_information(original)

    # Copy and rename file
    copy_file(original, copied)
    rename_file(copied, renamed)

    # Windows-specific behavior
    check_case_sensitivity(original)
    check_permissions(original)

    # Display disk usage
    disk_information(directory)

    # Display directory contents
    display_directory(directory)

    # Delete laboratory files
    print("\n===== DELETE OPERATIONS =====")

    renamed.unlink()
    print("Deleted:", renamed.name)

    original.unlink()
    print("Deleted:", original.name)

    directory.rmdir()
    print("Directory removed:", directory)

    print("\nFile-system demonstration completed successfully.")
