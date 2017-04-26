#!/usr/bin/env python3

import subprocess
import os


this_folder = os.path.dirname(os.path.realpath(__file__))
target_folder = this_folder + os.path.sep + "results" + os.path.sep

if not os.path.exists(target_folder):
    os.makedirs(target_folder)

scen1 = [
    "--delay-dl=300",
    "--delay-ul=300",
    "--trace-multiplyer-ul=0.3",
    "--trace-multiplyer-dl=0.6",
    "--delay-deviation-ul=0.1",
    "--delay-deviation-dl=2.5",
    "--bw-trace=udp-traces/storo_4x_700kbps_120s_tv.log"
]

scen2 = [
    "--delay-dl=300",
    "--delay-ul=300",
    "--trace-multiplyer-ul=0.3",
    "--trace-multiplyer-dl=0.6",
    "--loss-prob-move-to-burst-dl=1",
    "--loss-prob-move-to-gap-dl=3",
    "--loss-rate-burst-dl=70",
    "--delay-deviation-ul=0.1",
    "--delay-deviation-dl=2.5",
    "--bw-trace=udp-traces/storo_4x_700kbps_120s_tv.log"
]

scen3 = [
    "--delay-dl=300",
    "--delay-ul=300",
    "--trace-multiplyer-ul=0.1",
    "--trace-multiplyer-dl=0.2",
    "--delay-deviation-ul=0.1",
    "--delay-deviation-dl=2.5",
    "--bw-trace=udp-traces/storo_4x_700kbps_120s_tv.log"
]

scen4 = [
    "--delay-dl=150",
    "--delay-ul=150",
    "--trace-multiplyer-ul=0.3",
    "--trace-multiplyer-dl=0.6",
    "--delay-deviation-ul=0.1",
    "--delay-deviation-dl=2.5",
    "--bw-trace=udp-traces/storo_4x_700kbps_120s_tv.log"
]

scen5 = [
    "--delay-dl=300",
    "--delay-ul=300",
    "--trace-multiplyer-ul=0.6",
    "--trace-multiplyer-dl=1.2",
    "--delay-deviation-ul=0.1",
    "--delay-deviation-dl=2.5",
    "--bw-trace=udp-traces/storo_4x_700kbps_120s_tv.log"
]

scen6 = [
]

scen5 = [
    "--delay-dl=300",
    "--delay-ul=300",
    "--bandwidth-dl=10",
    "--bandwidth-ul=10"
]


scenarios = []
scenarios.append(scen1)
scenarios.append(scen2)
scenarios.append(scen3)
scenarios.append(scen4)
scenarios.append(scen5)
scenarios.append(scen6)

i = 1
for scen in scenarios:
    # Open connections
    subprocess.check_call(
        [this_folder + os.path.sep + "generate-stats"] +
        scen +
        ["--open-connection", "-h1",],
        stdout=open(target_folder + "scen" + str(i) + "_open_http1.json", "w+")
        )
    subprocess.check_call(
        [this_folder + os.path.sep + "generate-stats"] +
        scen +
        ["--open-connection", "-h2"],
        stdout=open(target_folder + "scen" + str(i) + "_open_http2.json", "w+")
        )
    subprocess.check_call(
        [this_folder + os.path.sep + "generate-stats"] +
        scen +
        ["--open-connection", "-q", "-pq"],
        stdout=open(target_folder + "scen" + str(i) + "_open_pq.json", "w+")
        )
    i += 1

i = 1
for scen in scenarios:
    # Closed connection
    subprocess.check_call(
        [this_folder + os.path.sep + "generate-stats"] +
        scen +
        ["-h1",],
        stdout=open(target_folder + "scen" + str(i) + "_close_http1.json", "w+")
        )
    subprocess.check_call(
        [this_folder + os.path.sep + "generate-stats"] +
        scen +
        ["-h2"],
        stdout=open(target_folder + "scen" + str(i) + "_close_http2.json", "w+")
        )
    subprocess.check_call(
        [this_folder + os.path.sep + "generate-stats"] +
        scen +
        ["-q", "-pq"],
        stdout=open(target_folder + "scen" + str(i) + "_close_pq.json", "w+")
        )
    i += 1

for i in range(1, len(scenarios)+1):
    for test_type in ["close", "open"]:
        subprocess.check_call(
            [
                this_folder + os.path.sep + "compare",
                target_folder + "scen" + str(i) + "_" + test_type + "_http1.json",
                target_folder + "scen" + str(i) + "_" + test_type + "_pq.json",
            ],
            stdout=open(target_folder + "comp_pq_http1_scen" + str(i) + "_" + test_type + ".txt", "w+")
        )
        subprocess.check_call(
            [
                this_folder + os.path.sep + "compare",
                target_folder + "scen" + str(i) + "_" + test_type + "_http2.json",
                target_folder + "scen" + str(i) + "_" + test_type + "_pq.json",
            ],
            stdout=open(target_folder + "comp_pq_http2_scen" + str(i) + "_" + test_type + ".txt", "w+")
        )
