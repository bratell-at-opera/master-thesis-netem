#!/bin/bash

this_folder=$(dirname $(realpath $0))
netem_folder=$(realpath $this_folder/..)
opera_controller="$this_folder/opera-controller.bash"
timeout=60

# Set extblog extension in bash in order for case-switch to work (disabled when executing script)
shopt -s extglob
# Handle in-arguments
for argument in "$@"
do
    case $argument in
        -q|--quic)
            web_protocol="--quic"
            shift
            ;;
        -h2|--http2)
            web_protocol="--http2"
            shift
            ;;
        -h1|--http1)
            web_protocol="--http1"
            shift
            ;;
        --timeout=*)
            timeout=${argument#*=}
            shift
            ;;
        --max-retries=*)
            :
            shift
            ;;
        --identifier=*)
            identifier=${argument#*=}
            shift
            ;;
        *)
            echo "$0: INVALID ARG: $argument"
            shift
            ;;
    esac
done

# Clear profile dir
profile_dir="/tmp/netem.opera"
rm -rf $profile_dir/*

# Start Opera
if [ "$web_protocol" = "--quic" ]; then
    opera --enable-quic --origin-to-force-quic-on=web.hfelo.se:443 --user-data-dir=$profile_dir --ignore-certificate-errors --disable-application-cache --host-resolver-rules="MAP * 192.168.100.1, EXCLUDE localhost" --disk-cache-size=0 about:blank &
else
    opera --user-data-dir=$profile_dir --ignore-certificate-errors --disable-application-cache --host-resolver-rules="MAP * 192.168.100.1, EXCLUDE localhost" --disk-cache-size=0 about:blank &
fi

sleep 2
$opera_controller --setup
sleep 2

# Enter URLS
while read url
do
    $opera_controller --go-to "https://web.hfelo.se/$url"
    sleep $timeout
    $opera_controller --save-stats $netem_folder/logs/hars/$identifier $url
done < $this_folder/../config/urls.txt


