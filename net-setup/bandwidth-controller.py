#!/usr/bin/env python3

import sys
import statistics
import subprocess
import time
import itertools
import re
import random


if len(sys.argv) not in [2, 3, 4]:
    sys.stderr.write("Incorrect no arguments. \n")
    sys.exit(1)

# constants
usec_sec = 1000000
usec_ms = 1000
bytes_to_MB = 1000000
bytes_to_bits = 8
second_average = 0.2

# In args
udp_trace_filename = sys.argv[1]
bw_down_mp = None
bw_up_mp = None

try:
    bw_down_mp = float(sys.argv[2])
    bw_up_mp = float(sys.argv[3])
except IndexError:
    pass

if not bw_down_mp:
    bw_down_mp = 1
if not bw_up_mp:
    bw_up_mp = 1

# Get the block size used, ugly hack
trace_contens = open(udp_trace_filename).read()
blocksize_regex = re.compile('blocksize \d+')
blocksize_match = blocksize_regex.findall(trace_contens)[0].split()[1]
block_size = int(blocksize_match)


# Get the running time of this trace
runn_time_regex = re.compile('\d+[s]')
time_match = runn_time_regex.findall(udp_trace_filename)
time_match = time_match[0].replace("s", "")
running_time = int(time_match)

bandwidth = []

with open(udp_trace_filename) as udp_trace_file:
    line = udp_trace_file.readline()
    columns = line.split()
    start_time = int(columns[2])
    last_packet_time = start_time
    last_packet_send_time = int(columns[1])
    multiplyer = 1
    receive_burst_size = 1
    last_packet_index = int(columns[0])

    for line in udp_trace_file:
        columns = line.split()
        if len(columns) == 3:
            packet_time = int(columns[2])
            packet_send_time = int(columns[1])
            packet_index = int(columns[0])
            time_delta = packet_time - last_packet_time

            # Look at bandwidth
            if time_delta == 0:
                multiplyer = multiplyer + 1
            else:
                current_bandwidth = multiplyer * \
                    (block_size / time_delta) * \
                    usec_sec / bytes_to_MB * \
                    bytes_to_bits

                bandwidth.append(current_bandwidth)

                multiplyer = 1
            last_packet_time = packet_time
            last_packet_send_time = packet_send_time
            last_packet_index = packet_index
        else:
            break

sys.stdout.write(udp_trace_filename +
                 " is a trace of length " +
                 time_match +
                 "s with a blocksize of " +
                 blocksize_match +
                 " bytes \n" +
                 "The average bandwidth of this trace is " +
                 str(statistics.mean(bandwidth)) +
                 "Mbit/s.\n\n")

# Get average bandwidth every n:th second
step_size = second_average / (running_time / len(bandwidth))
start_index = 0
end_index = round(step_size)
mplyer = 1
bandwidth_means = []

while end_index < len(bandwidth) - step_size:
    # Get data-points for mean
    points = bandwidth[start_index:end_index]
    bandwidth_means.append(statistics.mean(points))

    start_index = end_index
    mplyer = mplyer + 1
    end_index = round(mplyer * step_size)

cycled_list = itertools.cycle(bandwidth_means)

# Sleep so that the links have time to configure themselves first
time.sleep(2)
buffer_size = 10000

for momental_bandwidth in cycled_list:
    bw_down = momental_bandwidth * bw_down_mp
    # Max of 10 packets and bw_down / kernel tick rate
    tbf_burst_size_down = random.randint(1, 10) * 1520
    if bw_down / 250 > tbf_burst_size_down:
        tbf_burst_size_down = bw_down / 250,

    bw_up = momental_bandwidth * bw_up_mp
    tbf_burst_size_up = random.randint(1, 10) * 1520
    if bw_up / 250 > tbf_burst_size_down:
        tbf_burst_size_up = bw_up / 250,

    # Vary bucket size in order to get different burst-sizes

    sys.stdout.write("Setting down bandwidth to " +
                     str(bw_down) +
                     " Mbit/s and up bandwidth to " +
                     str(bw_up) +
                     "Mbit/s \n")
    sys.stdout.flush()
    # Bandwidth both up/down as well as for
    # TBF at the end of chain
#    subprocess.check_call(["tc",
#                           "-s",
#                           "qdisc",
#                           "change",
#                           "dev",
#                           "veth2",
#                           "root",
#                           "handle",
#                           "1:0",
#                           "netem",
#                           "rate",
#                           str(bw_down) + "Mbit",
#                           "limit",
#                           str(buffer_size)])
    subprocess.check_call(["tc",
                           "-s",
                           "qdisc",
                           "change",
                           "dev",
                           "veth2",
                           "root",
                           "handle",
                           "1:0",
                           "tbf",
                           "burst",
                           str(tbf_burst_size_down),
                           "latency",
                           "1000ms",
                           "rate",
                           str(bw_down) + "Mbit"])

#    subprocess.check_call(["tc",
#                           "-s",
#                           "qdisc",
#                           "change",
#                           "dev",
#                           "veth3",
#                           "root",
#                           "handle",
#                           "1:0",
#                           "netem",
#                           "rate",
#                           str(bw_up) + "Mbit"])
    subprocess.check_call(["tc",
                           "-s",
                           "qdisc",
                           "change",
                           "dev",
                           "veth3",
                           "root",
                           "handle",
                           "1:0",
                           "tbf",
                           "burst",
                           str(tbf_burst_size_up),
                           "latency",
                           "1000ms",
                           "rate",
                           str(bw_up) + "Mbit"])

    time.sleep(second_average)
