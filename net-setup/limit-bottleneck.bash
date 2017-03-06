#!/bin/bash
set -e

netem_folder=$(realpath $(dirname $0)/..)

# Handle in-arguments -------------
for argument in "$@"
do
    case $argument in
        "--loss-prob-move-to-gap-dl="*)
            loss_move_to_gap_dl="${argument#*=}"
            shift
            ;;
        "--loss-prob-move-to-burst-dl="*)
            loss_move_to_burst_dl="${argument#*=}"
            shift
            ;;
        "--loss-rate-burst-dl="*)
            loss_rate_dl="${argument#*=}"
            shift
            ;;
         "--loss-prob-move-to-gap-ul="*)
            loss_move_to_gap_ul="${argument#*=}"
            shift
            ;;
        "--loss-prob-move-to-burst-ul="*)
            loss_move_to_burst_ul="${argument#*=}"
            shift
            ;;
        "--loss-rate-burst-ul="*)
            loss_rate_ul="${argument#*=}"
            shift
            ;;
        "--delay-dl="*)
            mean_delay_down="${argument#*=}"
            shift
            ;;
        "--delay-deviation-dl="*)
            delay_deviation_down="${argument#*=}"
            shift
            ;;
        "--bandwidth-dl="*)
            bandwidth_down="${argument#*=}"
            shift
            ;;
        "--delay-ul="*)
            mean_delay_up="${argument#*=}"
            shift
            ;;
        "--delay-deviation-ul="*)
            delay_deviation_up="${argument#*=}"
            shift
            ;;
        "--bandwidth-ul="*)
            bandwidth_up="${argument#*=}"
            shift
            ;;
        "--bw-trace="*)
            trace=${argument#*=}
            shift
            ;;
        "--trace-multiplyer-ul="*)
            trace_mp_up=${argument#*=}
            shift
            ;;
        "--trace-multiplyer-dl="*)
            trace_mp_down=${argument#*=}
            shift
            ;;
        *)
            echo "$0 : Invalid argument $argument."
            exit 1
            shift
            ;;
    esac
done


# Check that arguments make sense
if [ -z "$loss_rate_dl" ] || [ -z "$loss_move_to_gap_dl" ] || [ -z "$loss_move_to_burst_dl" ]; then
    if [ -n "$loss_rate_dl" ] || [ -n "$loss_move_to_gap_dl" ] || [ -n "$loss_move_to_burst_dl" ]; then
        echo "You need to set all params regarding down-link loss in order to use down-link loss."
        exit 2
    fi
fi

if [ -z "$loss_rate_up" ] || [ -z "$loss_move_to_gap_up" ] || [ -z "$loss_move_to_burst_up" ]; then
    if [ -n "$loss_rate_up" ] || [ -n "$loss_move_to_gap_up" ] || [ -n "$loss_move_to_burst_up" ]; then
        echo "You need to set all params regarding up-link loss in order to use up-link loss."
        exit 2
    fi
fi

if [ -n "$trace" ] && ( [ -n "$bandwidth_down" ] || [ -n "$bandwidth_up" ] ); then
    echo "You can't both use a trace and specify a bandwidth limit!"
    exit 3
fi

# Used for restoring qdiscs
function restoreQdiscs () {
    for interface in $@; do
        tc qdisc replace dev $interface root fq_codel
        #tc qdisc del root dev $interface
    done
}

# Start by restoring qdiscs
restoreQdiscs "veth2" "veth3"

# Buffer size -------------------
buffer_size="250000"

# Setup the qdiscs -----------------------------------------------------
# Some nesting here but nessecary in order to set ordering correctly.
# Authors note: This looks like shit.
nrQdiscs=0

# Down-link -----------------------------
# Bandwidth

if [ -n "$trace" ]; then
    tc -s qdisc replace dev veth2 root handle 1:0 netem rate 0.5Mbit limit $buffer_size limit $buffer_size
    tc -s qdisc replace dev veth3 root handle 1:0 netem rate 0.5Mbit limit $buffer_size limit $buffer_size
    $netem_folder/net-setup/bandwidth-controller.py $trace $trace_mp_down $trace_mp_up &> $netem_folder/logs/bw-controller.log &
    bw_pid=$!
    bw_pid_file=/tmp/netem.bw-controller.pid
    touch $bw_pid_file
    echo $bw_pid > $bw_pid_file
    nrQdiscs=$(($nrQdiscs + 1))

elif [ -n "$bandwidth_down" ]; then
    if [ $nrQdiscs -gt 0 ]; then
        tc -s qdisc add dev veth2 parent $nrQdiscs:0 handle $(($nrQdiscs + 1)): netem rate "$bandwidth_down"Mbit limit $buffer_size
    else
        tc -s qdisc replace dev veth2 root handle 1:0 netem rate "$bandwidth_down"Mbit limit $buffer_size limit $buffer_size
    fi
    nrQdiscs=$(($nrQdiscs + 1))
fi

# Loss
if [ "$loss_move_to_burst_dl" ] && [ "$loss_move_to_gap_dl" ] && [ "$loss_rate_dl" ]; then
    if [ $nrQdiscs -gt 0 ]; then
        tcCommandLoss="tc -s qdisc add dev veth2 parent $nrQdiscs:0 handle $(($nrQdiscs + 1)):0 netem limit $buffer_size"
    else
        tcCommandLoss="tc -s qdisc replace dev veth2 root handle 1:0 netem limit $buffer_size"
    fi
    tcCommandLoss="$tcCommandLoss loss gemodel $loss_move_to_burst_dl% $loss_move_to_gap_dl% $loss_rate_dl% 0%"
    nrQdiscs=$(($nrQdiscs + 1))
fi

# Delay
tcCommandDelay=""
if [ $nrQdiscs -gt 0 ]; then
    tcCommandDelay="tc -s qdisc add dev veth2 parent $nrQdiscs:0 handle $(($nrQdiscs + 1)):0 netem limit $buffer_size"
else
    tcCommandDelay="tc -s qdisc replace dev veth2 root handle 1:0 netem limit $buffer_size"
fi


if [ -n "$mean_delay_down" ] && [ -n "$delay_deviation_down" ]; then
    tcCommandDelay="$tcCommandDelay delay "$mean_delay_down"ms "$delay_deviation_down"ms distribution normal"
    nrQdiscs=$(($nrQdiscs + 1))

elif [ -n "$mean_delay_down" ]; then
    tcCommandDelay="$tcCommandDelay delay "$mean_delay_down"ms"
    nrQdiscs=$(($nrQdiscs + 1))
elif [ -n "$delay_deviation_down" ] && [ -z "$mean_delay_down"]; then
    echo "ERROR: You can't set a delay deviation without setting a delay!!"
    restoreQdiscs veth2
    exit 11
fi

eval "$tcCommandLoss"
eval "$tcCommandDelay"

# Now do uplink! ---------------------------------------------------------------------
nrQdiscs=0
# Bandwidth
if [ -n "$trace" ]; then
    nrQdiscs=$(($nrQdiscs + 1))
elif [ -n "$bandwidth_up" ]; then
    if [ $nrQdiscs -gt 0 ]; then
        tc -s qdisc add dev veth3 parent $nrQdiscs:0 handle $(($nrQdiscs + 1)): netem rate "$bandwidth_up"Mbit limit $buffer_size
    else
        tc -s qdisc replace dev veth3 root handle 1:0 netem rate "$bandwidth_up"Mbit limit $buffer_size limit $buffer_size
    fi
    nrQdiscs=$(($nrQdiscs + 1))
fi

# Loss
tcCommandLoss=""
if [ "$loss_move_to_burst_ul" ] && [ "$loss_move_to_gap_ul" ] && [ "$loss_rate_ul" ]; then
    if [ $nrQdiscs -gt 0 ]; then
        tcCommandLoss="tc -s qdisc add dev veth3 parent $nrQdiscs:0 handle $(($nrQdiscs + 1)):0 netem limit $buffer_size"
    else
        tcCommandLoss="tc -s qdisc replace dev veth3 root handle 1:0 netem limit $buffer_size"
    fi
    tcCommandLoss="$tcCommandLoss loss gemodel $loss_move_to_burst_ul% $loss_move_to_gap_ul% $loss_rate_ul% 0%"
    nrQdiscs=$(($nrQdiscs + 1))
fi

# Delay
tcCommandDelay=""
if [ $nrQdiscs -gt 0 ]; then
    tcCommandDelay="tc -s qdisc add dev veth3 parent $nrQdiscs:0 handle $(($nrQdiscs + 1)):0 netem limit $buffer_size"
else
    tcCommandDelay="tc -s qdisc replace dev veth3 root handle 1:0 netem limit $buffer_size"
fi


if [ -n "$mean_delay_up" ] && [ -n "$delay_deviation_up" ]; then
    tcCommandDelay="$tcCommandDelay delay "$mean_delay_up"ms "$delay_deviation_up"ms distribution normal"
    nrQdiscs=$(($nrQdiscs + 1))

elif [ -n "$mean_delay_up" ]; then
    tcCommandDelay="$tcCommandDelay delay "$mean_delay_up"ms"
    nrQdiscs=$(($nrQdiscs + 1))
elif [ -n "$delay_deviation_up" ] && [ -z "$mean_delay_up"]; then
    echo "ERROR: You can't set a delay deviation without setting a delay!!"
    restoreQdiscs veth3
    exit 11
fi

eval "$tcCommandLoss"
eval "$tcCommandDelay"


# Enforce MTU sized packets only ---------------------------
ip netns exec server-ns ethtool --offload veth0 gso off
ip netns exec server-ns ethtool --offload veth0 tso off
ip netns exec server-ns ethtool --offload veth0 gro off

ethtool --offload veth2 gso off
ethtool --offload veth2 tso off
ethtool --offload veth2 gro off

ethtool --offload veth3 gso off
ethtool --offload veth3 tso off
ethtool --offload veth3 gro off

ip netns exec client-ns2 ethtool --offload veth5 gso off
ip netns exec client-ns2 ethtool --offload veth5 tso off
ip netns exec client-ns2 ethtool --offload veth5 gro off

