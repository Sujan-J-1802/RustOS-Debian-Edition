from pathlib import Path
import shutil


def list_files(directory):
    print("\nDirectory Contents:")

    for file in sorted(directory.iterdir()):
        print(file.name)


if __name__ == "__main__":

    print("File-System Interface Operations")
    print("=" * 50)

    # 1. Create a directory
    directory = Path("os_lab_demo")
    directory.mkdir(exist_ok=True)

    print("\n1. Directory created:", directory)

    # 2. Create a file
    file = directory / "sample.txt"
    file.write_text("Operating Systems Laboratory")

    print("\n2. File created:", file.name)

    # 3. Read a file
    print("\n3. Reading file:")
    print(file.read_text())

    # 4. Append data
    with file.open("a") as f:
        f.write("\nChapter 13 - File System Interface")

    print("\n4. Data appended successfully")
    print(file.read_text())

    # 5. List files
    print("\n5. Listing files")
    list_files(directory)

    # 6. Rename a file
    renamed_file = directory / "renamed.txt"
    file.rename(renamed_file)

    print("\n6. File renamed to:", renamed_file.name)

    # 7. Copy a file
    copied_file = directory / "backup.txt"
    shutil.copy(renamed_file, copied_file)

    print("\n7. File copied to:", copied_file.name)

    list_files(directory)

    # 8. Display file information
    print("\n8. File Information")
    print("File Name:", renamed_file.name)
    print("File Size:", renamed_file.stat().st_size, "bytes")
    print("File Exists:", renamed_file.exists())
    print("Is File:", renamed_file.is_file())

    # 9. Delete files
    renamed_file.unlink()
    copied_file.unlink()

    print("\n9. Files deleted successfully")

    # 10. Delete directory
    directory.rmdir()

    print("\n10. Directory deleted successfully")

    print("\nAll file-system operations completed.")
