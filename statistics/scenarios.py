#!/usr/bin/env python3

# Unlimited
scen8 = (
    "scen8",
    [])

# Bandwidth scenarios
scen10 = (
    "scen10",
    [
        "--bandwidth-dl=2",
        "--bandwidth-ul=1"
    ])

scen11 = (
    "scen11",
    [
        "--bandwidth-dl=0.5",
        "--bandwidth-ul=0.25"
    ])

scen12 = (
    "scen12",
    [
        "--trace-multiplyer-ul=1.2",
        "--trace-multiplyer-dl=2.4",
        "--bw-trace=udp-traces/storo_4x_700kbps_120s_tv.log"
    ])
scen13 = (
    "scen13",
    [
        "--trace-multiplyer-ul=0.6",
        "--trace-multiplyer-dl=1.2",
        "--bw-trace=udp-traces/storo_4x_700kbps_120s_tv.log"
    ])
scen14 = (
    "scen14",
    [
        "--bandwidth-dl=5",
        "--bandwidth-ul=3"
    ])
scen15 = (
    "scen15",
    [
        "--trace-multiplyer-ul=0.3",
        "--trace-multiplyer-dl=0.6",
        "--bw-trace=udp-traces/storo_4x_700kbps_120s_tv.log"
    ])

# Latency scenarios
scen20 = (
    "scen20",
    [
        "--delay-dl=300",
        "--delay-ul=300",
        "--bandwidth-dl=10",
        "--bandwidth-ul=10"
    ])
scen21 = (
    "scen21",
    [
        "--delay-dl=150",
        "--delay-ul=150",
        "--bandwidth-dl=10",
        "--bandwidth-ul=10"
    ])
scen22 = (
    "scen22",
    [
        "--delay-dl=75",
        "--delay-ul=75",
        "--bandwidth-dl=10",
        "--bandwidth-ul=10"
    ])
scen23 = (
    "scen23",
    [
        "--delay-dl=50",
        "--delay-ul=50",
        "--bandwidth-dl=10",
        "--bandwidth-ul=10"
    ])

# Latency variation scenario
scen30 = (
    "scen30",
    [
        "--delay-dl=50",
        "--delay-ul=50",
        "--delay-deviation-ul=0.1",
        "--delay-deviation-dl=2.5",
        "--bandwidth-dl=10",
        "--bandwidth-ul=10"
    ])

# Loss scenarios
scen40 = (
    "scen40",
    [
        "--bandwidth-dl=10",
        "--bandwidth-ul=10",
        "--loss-prob-move-to-burst-dl=1",
        "--loss-prob-move-to-gap-dl=3",
        "--loss-rate-burst-dl=70",
    ])
scen41 = (
    "scen41",
    [
        "--bandwidth-dl=10",
        "--bandwidth-ul=10",
        "--loss-prob-move-to-burst-dl=1",
        "--loss-prob-move-to-gap-dl=3",
        "--loss-rate-burst-dl=35",
    ])
scen42 = (
    "scen42",
    [
        "--bandwidth-dl=10",
        "--bandwidth-ul=10",
        "--loss-prob-move-to-burst-dl=1",
        "--loss-prob-move-to-gap-dl=3",
        "--loss-rate-burst-dl=10",
    ])

scenarios_defined = globals()
scenarios = []
bandwidth_scenarios = []
bandwidth_scenarios.append(scen8)
latency_scenarios = []
latency_scenarios.append(scen8)
loss_scenarios = []
loss_scenarios.append(scen8)

for i in range(1, 50):
    var_name = "scen" + str(i)
    if var_name in scenarios_defined:
        scenarios.append(scenarios_defined[var_name])

for i in range(10, 20):
    var_name = "scen" + str(i)
    if var_name in scenarios_defined:
        bandwidth_scenarios.append(scenarios_defined[var_name])

for i in range(20, 40):
    var_name = "scen" + str(i)
    if var_name in scenarios_defined:
        latency_scenarios.append(scenarios_defined[var_name])

for i in range(40, 50):
    var_name = "scen" + str(i)
    if var_name in scenarios_defined:
        loss_scenarios.append(scenarios_defined[var_name])
