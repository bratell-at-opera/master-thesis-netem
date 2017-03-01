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

    trace[str(last_index)] = dict()
    trace[str(last_index)]["recv_time"] = int(columns[2])
    trace[str(last_index)]["send_time"] = int(columns[1])
    trace[str(last_index)]["travel_time"] = \
        trace[str(last_index)]["recv_time"] - \
        trace[str(last_index)]["send_time"]

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
                (trace[str(index)]["recv_time"] -
                 trace[str(index)]["send_time"]) / \
                usec_ms

            # Calculate burst sizes
            if trace[str(last_index)]["recv_time"] != \
               trace[str(index)]["recv_time"]:
                trace["burst_sizes"].append(1)
                trace["bandwidths"].append(trace["packet_size"] /
                                           bytes_to_MB *
                                           bytes_to_bits)
                trace["recv_timestamps"].append(trace[str(index)]["recv_time"])
            else:
                trace["burst_sizes"][-1] = trace["burst_sizes"][-1] + 1
                trace["bandwidths"][-1] = trace["bandwidths"][-1] + \
                    trace["packet_size"] / bytes_to_MB * bytes_to_bits

            last_index = index
        else:
            trace["stop_index"] = last_index
            break

travel_times = []
timestamps = []
for index in range(trace["start_index"], trace["stop_index"] + 1):
    packet = trace[str(index)]
    if packet:
        travel_times.append(packet["travel_time"])
        timestamps.append(packet["recv_time"])

print("Mean bw: " + str(statistics.mean(trace["bandwidths"])) + " Mbits / sec")

print("Deviation in bw: " +
      str(statistics.stdev(trace["bandwidths"])) +
      " Mbit / sec")

print("Mean packet burst size: " + str(statistics.mean(trace["burst_sizes"])))

print("Deviation in burst sizes: " +
      str(statistics.stdev(trace["burst_sizes"])))
print("Mean packet travel time: " + str(statistics.mean(travel_times)) + " ms")
print("Deviation in travel time: " +
      str(statistics.stdev(travel_times)) +
      " ms")

plot.figure(1)
plot.plot(trace["recv_timestamps"], trace["bandwidths"])
plot.title("Instantanious bandwidth")
plot.xlabel("Time (s)")
plot.ylabel("Bandwidth (Mbit/s)")

runn_mean_n = 250
runn_mean = running_mean(trace["bandwidths"], runn_mean_n)
plot.figure(2)

plot.plot(trace["recv_timestamps"][0:len(runn_mean)], runn_mean)
plot.title("Running average bandwidth. N = " + str(runn_mean_n))
plot.xlabel("Time (s)")
plot.ylabel("Bandwidth (Mbit/s)")


plot.figure(3)
plot.plot(trace["recv_timestamps"], trace["burst_sizes"])
plot.title("Packet burst sizes")
plot.xlabel("Sequence")
plot.ylabel("Packets (nr)")

# plot.hold(True)
plot.figure(4)


plot.plot(timestamps, travel_times)
plot.title("Packet travel times")
plot.xlabel("Sequence")
plot.ylabel("Time (ms)")


plot.show()
