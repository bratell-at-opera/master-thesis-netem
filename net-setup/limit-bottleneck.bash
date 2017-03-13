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
            mean_delay_dl="${argument#*=}"
            shift
            ;;
        "--delay-deviation-dl="*)
            delay_deviation_dl="${argument#*=}"
            shift
            ;;
        "--bandwidth-dl="*)
            bandwidth_dl="${argument#*=}"
            shift
            ;;
        "--delay-ul="*)
            mean_delay_ul="${argument#*=}"
            shift
            ;;
        "--delay-deviation-ul="*)
            delay_deviation_ul="${argument#*=}"
            shift
            ;;
        "--bandwidth-ul="*)
            bandwidth_ul="${argument#*=}"
            shift
            ;;
        "--bw-trace="*)
            trace=${argument#*=}
            shift
            ;;
        "--trace-multiplyer-ul="*)
            trace_mp_ul=${argument#*=}
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

if [ -z "$loss_rate_ul" ] || [ -z "$loss_move_to_gap_ul" ] || [ -z "$loss_move_to_burst_ul" ]; then
    if [ -n "$loss_rate_ul" ] || [ -n "$loss_move_to_gap_ul" ] || [ -n "$loss_move_to_burst_ul" ]; then
        echo "You need to set all params regarding up-link loss in order to use up-link loss."
        exit 2
    fi
fi

if [ -n "$trace" ] && ( [ -n "$bandwidth_dl" ] || [ -n "$bandwidth_ul" ] ); then
    echo "You can't both use a trace and specify a bandwidth limit"
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
buffer_size="10000"

# Setup the qdiscs -----------------------------------------------------

# Down-link -----------------------------
# Bandwidth

if [ -n "$trace" ]; then
    tc -s qdisc replace dev veth2 root handle 1:0 tbf burst 16kbit latency 1000ms rate 2Mbit #netem limit $buffer_size
    tc -s qdisc replace dev veth3 root handle 1:0 tbf burst 16kbit latency 1000ms rate 2Mbit #netem limit $buffer_size
    $netem_folder/net-setup/bandwidth-controller.py $trace $trace_mp_down $trace_mp_ul &> $netem_folder/logs/bw-controller.log &
    bw_pid=$!
    bw_pid_file=/tmp/netem.bw-controller.pid
    touch $bw_pid_file
    echo $bw_pid > $bw_pid_file

elif [ -n "$bandwidth_dl" ]; then
    tc -s qdisc replace dev veth2 root handle 1:0 netem "$bandwidth_dl"Mbit limit $buffer_size
else
    tc -s qdisc replace dev veth2 root handle 1:0 netem limit $buffer_size
fi


# Loss
if [ "$loss_move_to_burst_dl" ] && [ "$loss_move_to_gap_dl" ] && [ "$loss_rate_dl" ]; then
    tc -s qdisc add dev veth2 parent 1:0 handle 2:0 netem loss gemodel $loss_move_to_burst_dl% $loss_move_to_gap_dl% $loss_rate_dl% 0% limit $buffer_size
else
    tc -s qdisc add dev veth2 parent 1:0 handle 2:0 netem limit $buffer_size
fi

# Delay
tcCommandDelay="tc -s qdisc add dev veth2 parent 2:0 handle 3:0 netem"

if [ -n "$mean_delay_dl" ] && [ -n "$delay_deviation_dl" ]; then
    tcCommandDelay="$tcCommandDelay delay "$mean_delay_dl"ms "$delay_deviation_dl"ms 50% distribution normal limit $buffer_size"

elif [ -n "$mean_delay_dl" ]; then
    tcCommandDelay="$tcCommandDelay" delay "$mean_delay_dl"ms
elif [ -n "$delay_deviation_dl" ] && [ -z "$mean_delay_dl"]; then
    echo "ERROR: You can not set a delay deviation without setting a delay!!"
    restoreQdiscs veth2
    exit 11
fi
eval "$tcCommandDelay"

## Add a TBF qdisc at the end of chain for burstier network
#if [ -n "$trace" ]; then
#    # Burst > bandwidth / kernel tick rate (250 Hz on Debian / Ubuntu)
#    tc -s qdisc add dev veth2 parent 3:0 handle 4:0 tbf burst 16kbit latency 2000ms rate 2Mbit
#
#elif [ -n "$bandwidth_dl" ]; then
#    # Burst = bandwidth / kernel tick rate (250 Hz on Debian / Ubuntu)
#    tc -s qdisc add dev veth2 parent 3:0 handle 4:0 tbf burst 16kbit latency 2000ms rate "$bandwidth_ul"Mbit
#fi

# Now do uplink! ---------------------------------------------------------------------
# Bandwidth
if [ -n "$trace" ]; then
    :
elif [ -n "$bandwidth_ul" ]; then
    # Burst size ~10 packets, min burst size ~1 packet (L2 MTU = L3 MTU + 14 bytes)
    tc -s qdisc replace dev veth3 root handle 1:0 tbf rate "$bandwidth_ul"Mbit limit $buffer_size
else
    tc -s qdisc replace dev veth3 root handle 1:0 netem limit $buffer_size
fi


# Loss
if [ "$loss_move_to_burst_ul" ] && [ "$loss_move_to_gap_ul" ] && [ "$loss_rate_ul" ]; then
    tc -s qdisc add dev veth3 parent 1:0 handle 2:0 netem loss gemodel $loss_move_to_burst_ul% $loss_move_to_gap_ul% $loss_rate_ul% 0% limit $buffer_size
else
    tc -s qdisc add dev veth3 parent 1:0 handle 2:0 netem limit $buffer_size
fi

# Delay
tcCommandDelay="tc -s qdisc add dev veth3 parent 2:0 handle 3:0 netem"

if [ -n "$mean_delay_ul" ] && [ -n "$delay_deviation_ul" ]; then
    tcCommandDelay="$tcCommandDelay delay "$mean_delay_ul"ms "$delay_deviation_ul"ms distribution normal limit $buffer_size"

elif [ -n "$mean_delay_ul" ]; then
    tcCommandDelay="$tcCommandDelay delay "$mean_delay_ul"ms"
elif [ -n "$delay_deviation_ul" ] && [ -z "$mean_delay_ul"]; then
    echo "ERROR: You can not set a delay deviation without setting a delay!!"
    restoreQdiscs veth3
    exit 11
fi
eval "$tcCommandDelay"

## Add a TBF qdisc at the end of chain for burstier network
#if [ -n "$trace" ]; then
#    # Burst > bandwidth / kernel tick rate (250 Hz on Debian / Ubuntu)
#    tc -s qdisc add dev veth3 parent 3:0 handle 4:0 tbf burst 16kbit latency 200ms rate 2Mbit
#
#elif [ -n "$bandwidth_ul" ]; then
#    # Burst = bandwidth / kernel tick rate (250 Hz on Debian / Ubuntu)
#    tc -s qdisc add dev veth3 parent 3:0 handle 4:0 tbf burst 16kbit latency 200ms rate "$bandwidth_ul"Mbit
#fi



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

