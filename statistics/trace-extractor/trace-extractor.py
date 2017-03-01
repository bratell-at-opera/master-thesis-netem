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
usec_sec = 1000000.0
usec_ms = 1000.0
bytes_to_MB = 1000000
bytes_to_bits = 8
udp_trace_filename = sys.argv[1]

trace = dict()
trace["burst_sizes"] = []
trace["bandwidths"] = []
trace["recv_timestamps"] = []
trace["packet_size"] = 1472

with open(udp_trace_filename) as udp_trace_file:
    line = udp_trace_file.readline()
    columns = line.split()

    last_index = int(columns[0])
    last_recv = int(columns[2])
    trace["start_index"] = last_index

    trace[str(index)]["recv_time"] = int(columns[2])
    trace[str(index)]["send_time"] = int(columns[1])
    trace[str(index)]["travel_time"] = \
    trace[str(index)]["recv_time"] - \
    trace[str(index)]["send_time"]
    trace[str(index)]["bandwidth"] = 0

    for line in udp_trace_file:
        columns = line.split()
        if len(columns) == 3:
            index = int(columns[0])
            trace[str(index)] = dict()
            diff = 0
            if index != last_index + 1:
                for i in range(last_index + 1, index):
                    trace[str(i)] = None

            trace[str(index)]["recv_time"] = int(columns[2])
            trace[str(index)]["send_time"] = int(columns[1])
            trace[str(index)]["travel_time"] = \
                trace[str(index)]["recv_time"] - \
                trace[str(index)]["send_time"]

            # Calculate burst sizes
            burst_size = 1
            for i in range(index, last_index):
                if trace[str(i)]["recv_time"] == \
                    trace[str(i - 1)]["recv_time"]:
                        burst_size = burst_size + 1
            if burst_size == 1:
                trace["burst_sizes"].append(burst_size)
                trace["bandwidths"].append(burst_size*trace["packet_size"])
                trace["recv_timestamps"].append(trace[str(index)]["recv_time"])
            else:
                trace["burst_sizes"][-1] = burst_size
                trace["bandwidths"][-1] = burst_size * trace["packet_size"]

            last_index = index
        else:
            trace["stop_index"] = last_index
            break


print("Mean bw: " + str(statistics.mean(trace["bandwidth"])) + " Mbits / sec")
print("Deviation in bw: " + str(statistics.stdev(trace["bandwidth"])) + " Mbit / sec")
print("Mean packet burst size: " + str(statistics.mean(trace["burst_sizes"])))
print("Deviation in burst sizes: " + str(statistics.stdev(trace["burst_sizes"])))
packet_travel_times = packet["travel_time"] if packet for packet in trace
print("Mean packet travel time: " + str(statistics.mean()) + " ms")
print("Deviation in travel time: " + str(statistics.stdev()) + " ms")

plot.figure(1)
plot.plot(time_list, bandwidth)
plot.title("Instantanious bandwidth")
plot.xlabel("Time (s)")
plot.ylabel("Bandwidth (Mbit/s)")

runn_mean_n = 250
runn_mean = running_mean(bandwidth, runn_mean_n)
plot.figure(2)

plot.plot(time_list[0:len(runn_mean)], runn_mean)
plot.title("Running average bandwidth. N = " + str(runn_mean_n))
plot.xlabel("Time (s)")
plot.ylabel("Bandwidth (Mbit/s)")


plot.figure(3)
plot.plot(range(0, len(packet_burst_sizes)), packet_burst_sizes)
plot.title("Packet burst sizes")
plot.xlabel("Sequence")
plot.ylabel("Packets (nr)")

# plot.hold(True)
plot.figure(4)
plot.plot(range(0, len(packet_travel_times) - 1), packet_travel_times[1:])
plot.title("Packet travel times")
plot.xlabel("Sequence")
plot.ylabel("Time (ms)")


plot.show()
