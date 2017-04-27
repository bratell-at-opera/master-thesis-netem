#!/usr/bin/env python3

import sys
import statistics
import subprocess
import time
import itertools
import re
import os


if len(sys.argv) not in [6, 7, 8]:
    sys.stderr.write("Incorrect no arguments. \n")
    sys.exit(1)

# constants
usec_sec = 1000000
usec_ms = 1000
bytes_to_MB = 1000000
bytes_to_bits = 8
second_average = 1

devation_params = {
    "5": 1.64,
    "2.5": 1.96,
    "0.1": 3.1,
    "0": 1000,
}

# In args
udp_trace_filename = sys.argv[1]
delay_down = int(sys.argv[2])
delay_up = int(sys.argv[3])
delay_deviation_down = sys.argv[4]
delay_deviation_up = sys.argv[5]
bw_down_mp = None
bw_up_mp = None
deviation_param_down = None
deviation_param_up = None

try:
    print(sys.argv)
    deviation_param_down = devation_params[delay_deviation_down]
    deviation_param_up = devation_params[delay_deviation_up]
except KeyError:
    sys.stderr.write("No entry for delay deviation.\n")
    sys.exit(1)

try:
    bw_down_mp = float(sys.argv[6])
    bw_up_mp = float(sys.argv[7])
except IndexError:
    pass

if not bw_down_mp:
    bw_down_mp = 1
if not bw_up_mp:
    bw_up_mp = 1

# Get ns identifier
ns_identifier = None
this_folder = os.path.dirname(os.path.realpath(__file__))
identifier_filename = this_folder + \
    os.path.sep + \
    ".." + \
    os.path.sep + \
    "identifiers.conf"

with open(identifier_filename) as identifier_file:
    for line in identifier_file:
        print(line)
        if "ns_identifier" in line:
            ns_identifier = line.split("=")[1].replace("\'", "").strip()

print(ns_identifier)

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

mean_bandwidth = statistics.mean(bandwidth)
sys.stdout.write(udp_trace_filename +
                 " is a trace of length " +
                 time_match +
                 "s with a blocksize of " +
                 blocksize_match +
                 " bytes \n" +
                 "The average bandwidth of this trace is " +
                 str(mean_bandwidth) +
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

# Create a distribution of packet burst sizes
# The probability of packet burst (n+1) is equal to
# round(P(n)/2)
burst_size_population = []
times = 100
for i in range(2, 10):
    for dummy in range(0, times):
        burst_size_population.append(i)
    times = round(times / 2)

for momental_bandwidth in cycled_list:
    bw_down = momental_bandwidth * bw_down_mp
    bw_up = momental_bandwidth * bw_up_mp

    # Calculate delay distribution. See master thesis for details
    nfive_perc_limit_down = (1 / ((bw_down * 1000000) / (8.0 * 1500.0))) / 2.0
    delay_sigma_down = (nfive_perc_limit_down / deviation_param_down) * 1000

    nfive_perc_limit_up = (1 / ((bw_up * 1000000) / (8.0 * 1500.0))) / 2.0
    delay_sigma_up = (nfive_perc_limit_up / deviation_param_up) * 1000

    # Just debug stuff
    sys.stdout.write("Setting down bandwidth to " +
                     str(bw_down) +
                     " Mbit/s and up bandwidth to " +
                     str(bw_up) +
                     "Mbit/s \n")
    # sys.stdout.flush()
    # Down-link
    # Bandwidth
    subprocess.check_call(["tc",
                           "-s",
                           "qdisc",
                           "change",
                           "dev",
                           "veth2-" + ns_identifier,
                           "root",
                           "handle",
                           "1:0",
                           "netem",
                           "rate",
                           str(bw_down) + "Mbit",
                           "limit",
                           str(buffer_size)
                           ])
    # Latency distribution
    if delay_deviation_down != "0":
        subprocess.check_call(["tc",
                               "-s",
                               "qdisc",
                               "change",
                               "dev",
                               "veth2-" + ns_identifier,
                               "parent",
                               "2:0",
                               "handle",
                               "3:0",
                               "netem",
                               "delay",
                               str(delay_down) + "ms",
                               str(delay_sigma_down) + "ms",
                               "distribution",
                               "normal",
                               "limit",
                               str(buffer_size)
                               ])

    # Up
    # Bandwidth
    subprocess.check_call(["tc",
                           "-s",
                           "qdisc",
                           "change",
                           "dev",
                           "veth3-" + ns_identifier,
                           "root",
                           "handle",
                           "1:0",
                           "netem",
                           "limit",
                           str(buffer_size),
                           "rate",
                           str(bw_up) + "Mbit"])
    # LAtency distribution
    if delay_deviation_up != "0":
        subprocess.check_call(["tc",
                               "-s",
                               "qdisc",
                               "change",
                               "dev",
                               "veth3-" + ns_identifier,
                               "parent",
                               "2:0",
                               "handle",
                               "3:0",
                               "netem",
                               "delay",
                               str(delay_up) + "ms",
                               str(delay_sigma_up) + "ms",
                               "distribution",
                               "normal",
                               "limit",
                               str(buffer_size)
                               ])

    time.sleep(second_average)
