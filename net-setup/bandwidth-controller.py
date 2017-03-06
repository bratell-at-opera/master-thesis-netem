#!/usr/bin/env python3

import sys
import statistics

if len(sys.argv) != 2:
    sys.stderr.write("Incorrect no arguments. \n")
    sys.exit(1)

# constants
block_size = 1472
usec_sec = 1000000
usec_ms = 1000
bytes_to_MB = 1000000
bytes_to_bits = 8
udp_trace_filename = sys.argv[1]

packet_burst_sizes_recv = []
bandwidth = []
time_list = []
full_time_list = []
packet_received = []
latency = []
packet_list = []

with open(udp_trace_filename) as udp_trace_file:
    line = udp_trace_file.readline()
    columns = line.split()
    start_time = int(columns[2])
    last_packet_time = start_time
    last_packet_send_time = int(columns[1])
    multiplyer = 1
    receive_burst_size = 1
    last_packet_index = int(columns[0])
    packet_received.append(1)
    packet_list.append(last_packet_index)
    latency.append((last_packet_time - last_packet_send_time) / usec_ms)

    for line in udp_trace_file:
        columns = line.split()
        if len(columns) == 3:
            packet_time = int(columns[2])
            packet_send_time = int(columns[1])
            packet_index = int(columns[0])
            packet_list.append(packet_index)
            time_delta = packet_time - last_packet_time

            # Look at bandwidth
            if time_delta == 0:
                multiplyer = multiplyer + 1
                receive_burst_size = receive_burst_size + 1
                packet_burst_sizes_recv.append(0)
            else:
                packet_burst_sizes_recv.append(receive_burst_size)
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
            last_packet_send_time = packet_send_time
            last_packet_index = packet_index
        else:
            break

# Get average bandwidth every n:th second
start_index = 0
running_time = 120
second_average = 1
step_size = second_average / (running_time / len(bandwidth))
end_index = round(step_size)
mplyer = 1
bandwidth_means = []
bandwidth_means_time = []

while end_index < len(bandwidth) - step_size:
    # Get data-points for mean
    points = bandwidth[start_index:end_index]
    bandwidth_means.append(statistics.mean(points))
    # Get the time of middle sample
    half_diff = (end_index - start_index) / 2
    bandwidth_means_time.append(time_list[round(start_index + half_diff)])
    start_index = end_index
    mplyer = mplyer + 1
    end_index = round(mplyer * step_size)
