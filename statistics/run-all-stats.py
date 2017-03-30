#!/usr/bin/env python3

import subprocess


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

scenarios = []
scenarios.append(scen1)
scenarios.append(scen2)
scenarios.append(scen3)
scenarios.append(scen4)

i = 0
for scen in scenarios:
    # Open connections
    subprocess.check_call(
        ["./generate-stats"] +
        scen +
        ["--open-connection", "-h1",],
        stdout=open("/tmp/scen" + str(i) + "_open_http1.json", "w+")
        )
    subprocess.check_call(
        ["./generate-stats"] +
        scen +
        ["--open-connection", "-h2"],
        stdout=open("/tmp/scen" + str(i) + "_open_http2.json", "w+")
        )
    subprocess.check_call(
        ["./generate-stats"] +
        scen +
        ["--open-connection", "-q", "-pq"],
        stdout=open("/tmp/scen" + str(i) + "_open_pq.json", "w+")
        )

for scen in scenarios:
    # Closed connection
    subprocess.check_call(
        ["./generate-stats"] +
        scen +
        ["-h1",],
        stdout=open("/tmp/scen" + str(i) + "_close_http1.json", "w+")
        )
    subprocess.check_call(
        ["./generate-stats"] +
        scen +
        ["-h2"],
        stdout=open("/tmp/scen" + str(i) + "_close_http2.json", "w+")
        )
    subprocess.check_call(
        ["./generate-stats"] +
        scen +
        ["-q", "-pq"],
        stdout=open("/tmp/scen" + str(i) + "_close_pq.json", "w+")
        )
