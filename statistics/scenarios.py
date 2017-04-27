#!/usr/bin/env python3


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
    "--delay-dl=300",
    "--delay-ul=300",
    "--trace-multiplyer-ul=1.2",
    "--trace-multiplyer-dl=2.4",
    "--delay-deviation-ul=0.1",
    "--delay-deviation-dl=2.5",
    "--bw-trace=udp-traces/storo_4x_700kbps_120s_tv.log"
]

scen7 = [
    "--delay-dl=300",
    "--delay-ul=300",
    "--bandwidth-dl=10",
    "--bandwidth-ul=10"
]

# Unlimited
scen8 = [
]

scen9 = [
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
scenarios.append(scen7)
scenarios.append(scen8)
scenarios.append(scen9)

