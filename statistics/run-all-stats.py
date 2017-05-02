#!/usr/bin/env python3

import subprocess
import os
import sys
from scenarios import scenarios, \
    bandwidth_scenarios, \
    latency_scenarios, \
    loss_scenarios

this_folder = os.path.dirname(os.path.realpath(__file__))
target_folder = this_folder + os.path.sep + "results" + os.path.sep

if not os.path.exists(target_folder):
    os.makedirs(target_folder)

scenarios_to_check = scenarios
if len(sys.argv) > 1:
    if sys.argv[1] == "--bandwidth":
        scenarios_to_check = bandwidth_scenarios
    elif sys.argv[1] == "--loss":
        scenarios_to_check = loss_scenarios
    elif sys.argv[1] == "--latency":
        scenarios_to_check = latency_scenarios
    else:
        scenarios_to_check = scenarios


for scen in scenarios_to_check:
    # Open connections
    subprocess.check_call(
        [this_folder + os.path.sep + "generate-stats"] +
        scen[1] +
        ["--open-connection", "-h1"],
        stdout=open(
            target_folder +
            scen[0] +
            "_open_http1.json", "w+")
        )
    subprocess.check_call(
        [this_folder + os.path.sep + "generate-stats"] +
        scen[1] +
        ["--open-connection", "-h2"],
        stdout=open(
            target_folder +
            scen[0] +
            "_open_http2.json", "w+")
        )
    subprocess.check_call(
        [this_folder + os.path.sep + "generate-stats"] +
        scen[1] +
        ["--open-connection", "-q", "-pq"],
        stdout=open(
            target_folder +
            scen[0] +
            "_open_pq.json", "w+")
        )

for scen in scenarios_to_check:
    # Closed connection
    subprocess.check_call(
        [this_folder + os.path.sep + "generate-stats"] +
        scen[1] +
        ["-h1"],
        stdout=open(
            target_folder +
            scen[0] +
            "_close_http1.json", "w+")
        )
    subprocess.check_call(
        [this_folder + os.path.sep + "generate-stats"] +
        scen[1] +
        ["-h2"],
        stdout=open(
            target_folder +
            scen[0] +
            "_close_http2.json", "w+")
        )
    subprocess.check_call(
        [this_folder + os.path.sep + "generate-stats"] +
        scen[1] +
        ["-q", "-pq"],
        stdout=open(target_folder + scen[0] + "_close_pq.json", "w+")
        )

for scen in scenarios_to_check:
    for test_type in ["close", "open"]:
        subprocess.check_call(
            [
                this_folder + os.path.sep + "compare",
                target_folder +
                scen[0] +
                "_" +
                test_type +
                "_http1.json",
                target_folder +
                scen[0] +
                "_" +
                test_type +
                "_pq.json",
            ],
            stdout=open(
                target_folder +
                "comp_pq_http1_" +
                scen[0] +
                "_" +
                test_type +
                ".txt", "w+")
        )
        subprocess.check_call(
            [
                this_folder + os.path.sep + "compare",
                target_folder +
                scen[0] +
                "_" +
                test_type +
                "_http2.json",
                target_folder +
                scen[0] +
                "_" +
                test_type +
                "_pq.json",
            ],
            stdout=open(
                target_folder +
                "comp_pq_http2_" +
                scen[0] +
                "_" +
                test_type +
                ".txt", "w+")
        )
