#!/usr/bin/env python3

import sys
import statistics


if len(sys.argv) != 2:
    sys.stderr.write("Incorrect no arguments. \n")
    sys.exit(1)

# bytes
block_size = 1472
usec_sec = 1000000
udp_trace_filename = sys.argv[1]

bandwidth = []
time_list = []

with open(udp_trace_filename) as udp_trace_file:
    line = udp_trace_file.readline()
    columns = line.split()
    start_time = int(columns[2])
    last_packet_time = start_time
    multiplyer = 1

    for line in udp_trace_file:
        columns = line.split()
        if len(columns) == 3:
            packet_time = int(columns[2])
            time_delta = packet_time - last_packet_time

            if time_delta == 0:
                multiplyer = multiplyer + 1
            else:
                current_bandwidth = multiplyer * (block_size / time_delta) * usec_sec
                for i in range(0, multiplyer):
                    bandwidth.append(current_bandwidth)

                time_list.append(packet_time - start_time)
                multiplyer = 1
        else:
            break

print("Mean bw: " + str(statistics.mean(bandwidth)) + " bytes / sec")
print("Deviation in bw: " + str(statistics.stdev(bandwidth)))
