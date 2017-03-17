#!/bin/bash
set -e

netemFolder=$(realpath $(dirname $0))/..
hostname=$1
ns_identifier=$2

# Add two namespaces for server and client
ip netns add server-ns-$ns_identifier
ip netns add client-ns-$ns_identifier

# Add three virtual links with two interfaces each
# server -> switch 1
ip link add veth0-$ns_identifier type veth peer name veth1-$ns_identifier
# switch 1 -> switch 2
ip link add veth2-$ns_identifier type veth peer name veth3-$ns_identifier
# switch 2 -> client-2
ip link add veth4-$ns_identifier type veth peer name veth5-$ns_identifier

# Create switches
ovs-vsctl add-br switch1-$ns_identifier
ovs-vsctl add-br switch2-$ns_identifier

# Attach server interface to server ns
ip link set veth0-$ns_identifier netns server-ns-$ns_identifier
# Attach client interface(s)
ip link set veth5-$ns_identifier netns client-ns-$ns_identifier

# Attach interfaces to switches
ovs-vsctl add-port switch1-$ns_identifier veth1-$ns_identifier
ovs-vsctl add-port switch1-$ns_identifier veth2-$ns_identifier
ovs-vsctl add-port switch2-$ns_identifier veth3-$ns_identifier
ovs-vsctl add-port switch2-$ns_identifier veth4-$ns_identifier

# Up the links
ifconfig veth1-$ns_identifier up
ifconfig veth2-$ns_identifier up
ifconfig veth3-$ns_identifier up
ifconfig veth4-$ns_identifier up

# Set server ip
ip netns exec server-ns-$ns_identifier ifconfig veth0-$ns_identifier 192.168.100.1 mtu 1500
# Set client IP
ip netns exec client-ns-$ns_identifier ifconfig veth5-$ns_identifier 192.168.100.2 mtu 1500
ip netns exec client-ns-$ns_identifier ifconfig lo 127.0.0.1
ip netns exec client-ns-$ns_identifier ifconfig lo 127.0.1.1

# -----------------------------

