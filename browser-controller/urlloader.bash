#!/bin/bash

this_folder=$(dirname $(realpath $0))
opera_controller="$this_folder/opera-controller.bash"
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
        --loss-rate-@(dl|ul)=*)
            :
            shift
            ;;
        --delay-@(dl|ul)=*)
            :
            shift
            ;;
        --delay-deviation-@(dl|ul)=*)
            :
            shift
            ;;
        --bandwidth-@(dl|ul)=*)
            :
            shift
            ;;
        --timeout=*)
            :
            shift
            ;;
        --max-retries=*)
            :
            shift
            ;;
        *)
            echo "$0: INVALID ARG: $argument"
            shift
            ;;
    esac
done

# Start Opera
opera_options='--ignore-certificate-errors --disable-application-cache --host-resolver-rules="MAP * 192.168.100.1, EXCLUDE localhost" --disk-cache-size=0'

if [ "$web_protocol" = "--quic" ]; then
    opera_options="$opera_options --enable-quic --origin-to-force-quic-on=web.hfelo.se:443"
fi

opera $opera_options &
$opera_controller --setup

# Enter URLS
for url in $(cat $this_folder/../config/urls.txt); do
    $opera_controller --go-to $url
    sleep 60
    $opera_controller --save-stats $this_folder/logs/hars
done


