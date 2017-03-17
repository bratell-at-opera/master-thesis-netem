#!/bin/bash

netemFolder=$(realpath $(dirname $0))/..
source $netemFolder/identifiers.conf

# Remove the NICs
ip link del veth1-$ns_identifier
ip link del veth2-$ns_identifier
ip link del veth4-$ns_identifier

# Destroy switches
ovs-vsctl del-br switch1-$ns_identifier
ovs-vsctl del-br switch2-$ns_identifier

# Delete namespaces
ip netns delete server-ns-$ns_identifier
ip netns delete client-ns-$ns_identifier

