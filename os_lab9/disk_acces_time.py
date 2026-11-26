def calculate_access_time(seek_time, rpm, data_size, transfer_rate):

    rotational_latency = (60 / (2 * rpm)) * 1000

    transfer_time = (data_size / transfer_rate) * 1000

    access_time = seek_time + rotational_latency + transfer_time

    return rotational_latency, transfer_time, access_time


if __name__ == "__main__":
    seek_time = 8
    rpm = 7200
    data_size = 4
    transfer_rate = 150

    latency, transfer, total = calculate_access_time(
        seek_time, rpm, data_size, transfer_rate
    )

    print("Disk Access Time Simulation")
    print("=" * 50)

    print("Disk Speed:", rpm, "RPM")
    print("Data Size:", data_size, "MB")
    print("Transfer Rate:", transfer_rate, "MB/s")

    print("-" * 50)

    print(f"Seek Time:              {seek_time:.2f} ms")
    print(f"Rotational Latency:     {latency:.2f} ms")
    print(f"Transfer Time:          {transfer:.2f} ms")

    print("-" * 50)

    print(f"Total Disk Access Time: {total:.2f} ms")
