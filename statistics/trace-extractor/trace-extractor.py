#!/usr/bin/env python3

import sys
import statistics
import matplotlib.pyplot as plot
import math
import numpy as np


if len(sys.argv) != 2:
    sys.stderr.write("Incorrect no arguments. \n")
    sys.exit(1)


def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / N


# bytes
block_size = 1472
usec_sec = 1000000
bytes_to_MB = 1000000
bytes_to_bits = 8
udp_trace_filename = sys.argv[1]

packet_burst_sizes = []
bandwidth = []
time_list = []
packet_received = []

with open(udp_trace_filename) as udp_trace_file:
    line = udp_trace_file.readline()
    columns = line.split()
    start_time = int(columns[1])
    last_packet_time = start_time
    multiplyer = 1
    receive_burst_size = 1
    last_packet_index = int(columns[0])
    packet_received.append(1)

    for line in udp_trace_file:
        columns = line.split()
        if len(columns) == 3:
            packet_time = int(columns[1])
            packet_send_time = int(columns[2])
            packet_index = int(columns[0])

            # Keep track of losses
            for packet in range(last_packet_index, packet_index):
                packet_received.append(0)
            packet_received.append(1)

            time_delta = packet_time - last_packet_time

            if time_delta == 0:
                multiplyer = multiplyer + 1
                receive_burst_size = receive_burst_size + 1
                packet_burst_sizes.append(0)
            else:
                packet_burst_sizes.append(receive_burst_size)
                receive_burst_size = 1

                current_bandwidth = multiplyer * \
                    (block_size / time_delta) * \
                    usec_sec / bytes_to_MB * \
                    bytes_to_bits
                for i in range(0, multiplyer):
                    bandwidth.append(current_bandwidth)

                time_list.append((packet_time - start_time) / usec_sec)

                multiplyer = 1
                last_packet_time = packet_time
        else:
            break

print("Mean bw: " + str(statistics.mean(bandwidth)) + " Mbits / sec")
print("Deviation in bw: " + str(statistics.stdev(bandwidth)) + " Mbit / sec")
print("Mean packet burst size: " + str(statistics.mean(packet_burst_sizes)))
print("Deviation in burst sizes: " + str(statistics.stdev(packet_burst_sizes)))

plot.figure(1)
plot.plot(time_list, bandwidth)
plot.title("Instantanious bandwidth")
plot.xlabel("Time (s)")
plot.ylabel("Bandwidth (Mbit/s)")

runn_mean_n = 100
runn_mean = running_mean(bandwidth, runn_mean_n)
edges = (len(time_list) - len(runn_mean)) / 2
adder = 0
if not (edges).is_integer():
    edges = math.floor(edges)
    adder = -1

plot.figure(2)
plot.plot(time_list[edges:len(time_list) - edges + adder], runn_mean)
plot.title("Running average bandwidth. N = " + str(runn_mean_n))
plot.xlabel("Time (s)")
plot.ylabel("Bandwidth (Mbit/s)")


plot.figure(3)
plot.plot(time_list, packet_burst_sizes, "ko", markersize=2)
plot.title("Packet burst sizes")
plot.xlabel("Time (s)")
plot.ylabel("Packets (nr)")


plot.figure(4)
plot.plot(range(0, len(packet_received)), packet_received, "ko", markersize=2)
plot.title("Packet arrived")
plot.xlabel("Arrived packets")
plot.ylabel("Sequence nr")

plot.show()
