# RustOS Debian Edition v6.1

A customized Debian 13 (Trixie) live operating system
developed for a university Operating Systems project.

## Overview

RustOS Debian Edition v6.1 is built using Debian
live-build and provides an XFCE desktop, networking,
package management, Snap Store integration, hardware
diagnostics, persistence support, and automatic boot
performance measurement.

This project is a customized Debian-based distribution,
not a new operating-system kernel written in Rust.

## Features

- Debian GNU/Linux 13 (Trixie)
- XFCE graphical desktop
- Ethernet and WiFi networking support
- NetworkManager and wireless firmware packages
- APT and Aptitude package managers
- Snap Store integration
- Offline Snap package provisioning
- Persistent live filesystem support
- Hardware diagnostic utilities
- Automatic boot-time benchmarking
- VirtualBox compatibility

## Project Structure

Dockerfile
  Docker-based Debian build environment

auto/
  Debian live-build configuration

config/
  Package lists, custom scripts, desktop launchers,
  systemd services, timers, and build configuration

## Build Environment

- Windows 11 with Ubuntu WSL2
- Docker Desktop
- Debian 13 (Trixie)
- Debian live-build
- Oracle VirtualBox

## Build Instructions

Build the Docker environment:

    docker build -t rustos-builder:trixie-final .

Build the live ISO:

    docker run --rm --privileged \
      --platform linux/amd64 \
      -v "$PWD:/work" \
      -w /work \
      rustos-builder:trixie-final \
      bash -lc 'lb config && lb build'

Note: The original build included additional offline
Snap packages. These binary assets are excluded from
this Git repository and must be restored to their
original paths for an equivalent offline-enabled build.

## VirtualBox Testing

The tested virtual machine configuration used:

- 2 virtual CPUs
- 2048 MB RAM
- VMSVGA graphics
- NAT networking
- RustOS-v6.1 ISO attached as a virtual DVD
- Separate ext4 persistence disk

## Boot Performance

Automatic boot measurements recorded:

| Boot | Kernel | Userspace | Total |
|------|--------|-----------|-------|
| 1 | 9.662 s | 6.176 s | 15.838 s |
| 2 | 10.621 s | 6.427 s | 17.048 s |

Average boot time: **16.443 seconds**

Measurements were collected in Oracle VirtualBox
using systemd-analyze and a custom Python recorder.

## Testing Status

Verified:
- Booting the live ISO in VirtualBox
- XFCE desktop
- Virtual Ethernet connectivity
- APT/Aptitude installation
- Snap Store package provisioning
- Persistent storage
- Automatic boot benchmarking

Not fully verified:
- Physical laptop hardware compatibility
- Connection through a physical WiFi adapter
- Complete graphical Snap Store installation workflow

## Project Submission

The bootable ISO is distributed separately through
Google Drive because of its size.

The offline Snap binary dependencies are also
distributed separately from this Git repository.

## License

No license has been assigned.

## Offline Snap Dependencies

The RustOS v6.1 build uses six offline Snap packages
and their corresponding assertion files.

These large binary dependencies are excluded from GitHub.

### Required Packages

| Package | Revision |
|---------|----------|
| bare | 5 |
| core24 | 2307 |
| gnome-46-2404 | 184 |
| gtk-common-themes | 1535 |
| mesa-2404 | 1839 |
| snap-store | 1509 |

### Dependency Archive

Filename: `rustos-v6.1-offline-snaps.tar.gz`

The archive contains 6 `.snap` files and 6 `.assert` files.

SHA-256:

`65b6c20971a83e9e4628f94a65ba4bc7b8343e7cae73b13378d85e7ace8076ca`

The archive will be distributed separately.
The download link will be added after uploading.

### Restore Dependencies

Clone the repository:

    git clone https://github.com/Sujan-J-1802/RustOS-Debian-Edition.git
    cd RustOS-Debian-Edition

Copy the downloaded archive into the repository directory.

Verify its checksum:

    sha256sum rustos-v6.1-offline-snaps.tar.gz

Compare the output with the SHA-256 value above.

Extract the dependencies:

    tar -xzf rustos-v6.1-offline-snaps.tar.gz

This restores the packages to:

    config/includes.chroot/opt/rustos/snap-packages/

Verify the file count:

    find config/includes.chroot/opt/rustos/snap-packages \
      -maxdepth 1 -type f | wc -l

Expected result: 12 files.

### Build the Offline-Enabled ISO

Build the Docker environment:

    docker build -t rustos-builder:trixie-final .

Build the ISO:

    docker run --rm --privileged \
      --platform linux/amd64 \
      -v "$PWD:/work" \
      -w /work \
      rustos-builder:trixie-final \
      bash -lc 'lb config && lb build'

A successful build also depends on the required Debian
repositories and build environment being available.

### Runtime Requirements

Offline Snap provisioning requires a persistent live
filesystem. The installer checks for persistence and
sufficient writable storage before installing packages.
