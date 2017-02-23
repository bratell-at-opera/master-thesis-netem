#!/bin/bash

this_folder=$(dirname $(realpath $0))
netem_folder=$(realpath $this_folder/..)
opera_controller="$this_folder/opera-controller.bash"
timeout=60
max_retries=3

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
        -pq|--proto-quic)
            proto_quic=true
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
            max_retries=${argument#*=}
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
    opera --enable-quic --origin-to-force-quic-on=web.hfelo.se:443 --user-data-dir=$profile_dir --ignore-certificate-errors --disable-application-cache --host-resolver-rules="MAP * 192.168.100.1, EXCLUDE localhost" --disk-cache-size=0 about:blank &> /dev/null &
else
    opera --user-data-dir=$profile_dir --ignore-certificate-errors --disable-application-cache --host-resolver-rules="MAP * 192.168.100.1, EXCLUDE localhost" --disk-cache-size=0 about:blank &> /dev/null &
fi

sleep 2
$opera_controller --setup
sleep 2

# Enter URLS
while read url
do
    failed=0
    while true
    do
        if [ "$proto_quic" = true ]; then
            $opera_controller --go-to "https://web.hfelo.se/files/$url"
        else
            $opera_controller --go-to "https://web.hfelo.se/$url"
        fi
        sleep $timeout
        $opera_controller --save-stats $netem_folder/logs/hars/$identifier $url

        # Check if we succeeded in saving this site - otherwise retry
        if [ ! -f "$netem_folder/logs/hars/$identifier/$url.har" ] && [ "$failed" -lt "$max_retries" ]
        then
            echo "Failed fetching $url"
            failed=$(( $failed + 1 ))
            killall opera
            rm -rf $profile_dir/*

            if [ "$web_protocol" = "--quic" ]; then
                opera --enable-quic --origin-to-force-quic-on=web.hfelo.se:443 --user-data-dir=$profile_dir --ignore-certificate-errors --disable-application-cache --host-resolver-rules="MAP * 192.168.100.1, EXCLUDE localhost" --disk-cache-size=0 about:blank &> /dev/null &
            else
                opera --user-data-dir=$profile_dir --ignore-certificate-errors --disable-application-cache --host-resolver-rules="MAP * 192.168.100.1, EXCLUDE localhost" --disk-cache-size=0 about:blank &> /dev/null &
            fi
            sleep 2
            $opera_controller --setup
            sleep 2
        else
            break
        fi
    done
done < $this_folder/../config/urls.txt


