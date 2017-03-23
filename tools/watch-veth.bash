#!/bin/bash

for netns in $(ip netns | awk '{print $1}' | tr "-" " " | awk '{print $3}' | uniq)
    do tc -s qdisc show dev veth2-$netns | grep netem
    echo -----------
done
