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

            # Keep track of latency variations
            time_delta = packet_time - last_packet_time
            latency.append((packet_time - packet_send_time) - usec_ms)

            # Keep track of losses
            for packet in range(last_packet_index + 1, packet_index):
                packet_received.append(0)
                full_time_list.append(packet_time - start_time)
            packet_received.append(1)
            full_time_list.append(packet_time - start_time)

            # Look at bandwidth
            if time_delta <= 10000:
                multiplyer = multiplyer + 1
                receive_burst_size = receive_burst_size + 1
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

print("Mean bw: " + str(statistics.mean(bandwidth)) + " Mbits / sec")
print("Deviation in bw: " + str(statistics.stdev(bandwidth)) + " Mbit / sec")
print("Mean packet burst size: " +
      str(statistics.mean(packet_burst_sizes_recv)))
print("Deviation in burst sizes: " +
      str(statistics.stdev(packet_burst_sizes_recv)))
print("Mean packet loss:" +
      str(statistics.mean(packet_received)))
print("Deviation in packet_loss:" +
      str(statistics.stdev(packet_received)))

# Bandwidth
plot.figure(1)
plot.plot(time_list, bandwidth)
plot.title("Instantanious bandwidth")
plot.xlabel("Time (s)")
plot.ylabel("Bandwidth (Mbit/s)")

# Get average bandwidth every second
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

plot.figure(2)
plot.plot(bandwidth_means_time, bandwidth_means)
plot.title("Average bandwidth every " + str(second_average) + " seconds")
plot.xlabel("Time (s)")
plot.ylabel("Bandwidth (Mbit/s)")


plot.figure(3)
plot.plot(range(0, len(packet_burst_sizes_recv)),
          packet_burst_sizes_recv,
          "ko",
          markersize=2)
plot.title("Packet burst sizes")
plot.xlabel("Time (s)")
plot.ylabel("Packets (nr)")

# Latency variations
latency_mean = statistics.mean(latency)
latency_compared_to_mean = []
for value in latency:
    latency_compared_to_mean.append(value - latency_mean)

plot.figure(5)
plot.plot(packet_list, latency_compared_to_mean)
plot.title("Variance in link latency")
plot.xlabel("Packet nr")
plot.ylabel(
    "Travel time difference between \nmean and current packet (ms)"
)

# Packet loss running mean
loss_runn_n = 100
packet_loss_runn_mean = running_mean(packet_received, loss_runn_n)
edges = (len(full_time_list) - len(packet_loss_runn_mean)) / 2
adder = 0
if not (edges).is_integer():
    edges = math.floor(edges)
    adder = -1
edges = int(edges)

plot.figure(4)
plot.plot(range(0, len(packet_loss_runn_mean)),
          packet_loss_runn_mean,
          markersize=2)
plot.title("Packet arrived percentage, running mean N=" +
           str(loss_runn_n))
plot.xlabel("Packet nr")
plot.ylabel("Arrive percentage")

plot.show()
