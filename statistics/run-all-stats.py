#!/usr/bin/env python3

import subprocess
import os
from scenarios import *

this_folder = os.path.dirname(os.path.realpath(__file__))
target_folder = this_folder + os.path.sep + "results" + os.path.sep

if not os.path.exists(target_folder):
    os.makedirs(target_folder)

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
