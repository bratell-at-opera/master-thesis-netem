#!/usr/bin/env python3

# Unlimited
scen8 = (
    "scen8",
    [],
    "Unlimited"
    )

# Poor network
scen7 = (
    "scen7",
    [
        "--delay-dl=300",
        "--delay-ul=300",
        "--delay-deviation-ul=0.1",
        "--delay-deviation-dl=2.5",
        "--trace-multiplyer-ul=0.3",
        "--trace-multiplyer-dl=0.6",
        "--bw-trace=udp-traces/storo_4x_700kbps_120s_tv.log"
    ],
    "Heavily limited"
    )


# Bandwidth scenarios
scen11 = (
    "scen11",
    [
        "--bandwidth-dl=2",
        "--bandwidth-ul=1"
    ],
    "M bw"
    )

scen12 = (
    "scen12",
    [
        "--bandwidth-dl=0.5",
        "--bandwidth-ul=0.25"
    ],
    "L bw"
    )

scen13 = (
    "scen13",
    [
        "--trace-multiplyer-ul=1.2",
        "--trace-multiplyer-dl=2.4",
        "--bw-trace=udp-traces/storo_4x_700kbps_120s_tv.log"
    ],
    "H trace"
    )

scen14 = (
    "scen14",
    [
        "--trace-multiplyer-ul=0.6",
        "--trace-multiplyer-dl=1.2",
        "--bw-trace=udp-traces/storo_4x_700kbps_120s_tv.log"
    ],
    "M trace"
    )

scen10 = (
    "scen10",
    [
        "--bandwidth-dl=5",
        "--bandwidth-ul=3"
    ],
    "H bw"
    )

scen15 = (
    "scen15",
    [
        "--trace-multiplyer-ul=0.3",
        "--trace-multiplyer-dl=0.6",
        "--bw-trace=udp-traces/storo_4x_700kbps_120s_tv.log"
    ],
    "L trace"
    )

# Latency scenarios
scen23 = (
    "scen23",
    [
        "--delay-dl=300",
        "--delay-ul=300",
        "--bandwidth-dl=10",
        "--bandwidth-ul=10"
    ],
    "H latency"
    )
scen22 = (
    "scen22",
    [
        "--delay-dl=150",
        "--delay-ul=150",
        "--bandwidth-dl=10",
        "--bandwidth-ul=10"
    ],
    "M latency"
    )

scen21 = (
    "scen21",
    [
        "--delay-dl=75",
        "--delay-ul=75",
        "--bandwidth-dl=10",
        "--bandwidth-ul=10"
    ],
    "L latency"
    )
scen20 = (
    "scen20",
    [
        "--delay-dl=50",
        "--delay-ul=50",
        "--bandwidth-dl=10",
        "--bandwidth-ul=10"
    ],
    "T latency"
    )

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
    ],
    "Varying latency"
    )

# Loss scenarios
scen42 = (
    "scen42",
    [
        "--bandwidth-dl=10",
        "--bandwidth-ul=10",
        "--loss-prob-move-to-burst-dl=1",
        "--loss-prob-move-to-gap-dl=3",
        "--loss-rate-burst-dl=70",
    ],
    "H loss"
    )

scen41 = (
    "scen41",
    [
        "--bandwidth-dl=10",
        "--bandwidth-ul=10",
        "--loss-prob-move-to-burst-dl=1",
        "--loss-prob-move-to-gap-dl=3",
        "--loss-rate-burst-dl=35",
    ],
    "M loss"
    )
scen40 = (
    "scen40",
    [
        "--bandwidth-dl=10",
        "--bandwidth-ul=10",
        "--loss-prob-move-to-burst-dl=1",
        "--loss-prob-move-to-gap-dl=3",
        "--loss-rate-burst-dl=10",
    ],
    "L loss"
    )

scenarios_defined = globals()
scenarios = []
baseline_scenarios = []
bandwidth_scenarios = []
latency_scenarios = []
loss_scenarios = []

for i in range(1, 50):
    var_name = "scen" + str(i)
    if var_name in scenarios_defined:
        scenarios.append(scenarios_defined[var_name])

for i in range(1, 10):
    var_name = "scen" + str(i)
    if var_name in scenarios_defined:
        baseline_scenarios.append(scenarios_defined[var_name])

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


differing_scenarios = []
differing_scenarios.append(scenarios_defined["scen8"])
differing_scenarios.append(scenarios_defined["scen20"])
differing_scenarios.append(scenarios_defined["scen23"])
