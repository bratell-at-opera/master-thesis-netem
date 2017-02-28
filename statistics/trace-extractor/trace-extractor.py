#!/usr/bin/env python3

import sys
import statistics
import matplotlib.pyplot as plot
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

bandwidth = []
time_list = []

with open(udp_trace_filename) as udp_trace_file:
    line = udp_trace_file.readline()
    columns = line.split()
    start_time = int(columns[1])
    last_packet_time = start_time
    multiplyer = 1

    for line in udp_trace_file:
        columns = line.split()
        if len(columns) == 3:
            packet_time = int(columns[1])
            time_delta = packet_time - last_packet_time

            if time_delta == 0:
                multiplyer = multiplyer + 1
            else:
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

plot.figure(1)
plot.plot(time_list, bandwidth)
plot.title("Instantanious bandwidth")
plot.xlabel("Time (s)")
plot.ylabel("Bandwidth (Mbit/s)")

runn_mean_n = 100
runn_mean = running_mean(bandwidth, runn_mean_n)
plot.figure(2)
plot.plot(time_list[0:len(runn_mean)], runn_mean)
plot.title("Running average bandwidth. N = " + str(runn_mean_n))
plot.xlabel("Time (s)")
plot.ylabel("Bandwidth (Mbit/s)")
plot.show()
