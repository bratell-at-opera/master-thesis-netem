#!/bin/bash

# Close all caddy-instances
for caddy in $(ps aux | grep caddy | grep -v "grep" | awk '{print $2}')
do
    echo "Killing caddy process"
    sudo kill $caddy
done


# close all proto-quic-instances
for proto_quic in $(ps aux | grep quic-server | grep -v "grep" | awk '{print $2}')
do
    echo "Killing proto-quic process"
    sudo kill $proto_quic
done

# Close all bandwidth controllers
for controller in $(ps aux | grep bandwidth-controller.py | grep -v "grep" | awk '{print $2}')
do
    echo "Killing bandwidth controller process"
    sudo kill $controller
done


