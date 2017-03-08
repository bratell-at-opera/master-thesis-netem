#!/bin/bash
set -e

netemFolder=$(realpath $(dirname $0))/..
hostname=$1

# Add two namespaces for server and client
ip netns add server-ns
ip netns add client-ns2

# Add three virtual links with two interfaces each
# server -> switch 1
ip link add veth0 type veth peer name veth1
# switch 1 -> switch 2
ip link add veth2 type veth peer name veth3
# switch 2 -> client-2
ip link add veth4 type veth peer name veth5

# Create switches
ovs-vsctl add-br switch1
ovs-vsctl add-br switch2

# Attach server interface to server ns
ip link set veth0 netns server-ns
# Attach client interface(s)
ip link set veth5 netns client-ns2

# Attach interfaces to switches
ovs-vsctl add-port switch1 veth1
ovs-vsctl add-port switch1 veth2
ovs-vsctl add-port switch2 veth3
ovs-vsctl add-port switch2 veth4

# Up the links
ifconfig veth1 up
ifconfig veth2 up
ifconfig veth3 up
ifconfig veth4 up

# Set server ip
ip netns exec server-ns ifconfig veth0 192.168.100.1 mtu 1500
# Set client IP
ip netns exec client-ns2 ifconfig veth5 192.168.100.2 mtu 1500
ip netns exec client-ns2 ifconfig lo 127.0.0.1
ip netns exec client-ns2 ifconfig lo 127.0.1.1

# -----------------------------

