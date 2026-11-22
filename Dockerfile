FROM debian:trixie-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    live-build \
    debootstrap \
    xorriso \
    grub-pc-bin \
    grub-efi-amd64-bin \
    isolinux \
    syslinux-common \
    squashfs-tools \
    mtools \
    dosfstools \
    rsync \
    ca-certificates \
    curl \
    file \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work

CMD ["bash"]
