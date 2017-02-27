#!/bin/bash


this_folder=$(dirname $(realpath $0))
netem_folder=$(realpath $this_folder/..)
opera_controller="$this_folder/opera-controller.bash"
timeout=60
max_retries=3
with_gui=false
debug_mode=false

browser=opera
# Clear profile dir
profile_dir="/tmp/netem.$browser"
rm -rf $profile_dir/*

# Read hostname from hostnamefile made by configure script
source $this_folder/hostname.conf

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
        --browser=*)
            browser=${argument#*=}
            shift
            ;;
        -g|--with-gui)
            with_gui=true
            shift
            ;;
        -d|--debug)
            debug_mode=true
            with_gui=true
            shift
            ;;
        *)
            echo "$0: INVALID ARG: $argument"
            shift
            ;;
    esac
done

function start-browser {
    browser=$1
    profile_dir=$2
    hostname=$3
    with_gui=$4
    protocol=$5

    # Clear profile
    rm -rf $profile_dir

    if [ "$with_gui" = false ]; then
        browser="xvfb-run --auto-servernum $browser"
    fi

    if [ "$protocol" = "--quic" ]; then
        $browser --enable-benchmarking --enable-net-benchmarking --remote-debugging-port=9222 --enable-quic --origin-to-force-quic-on=$hostname:443 --user-data-dir=$profile_dir --ignore-certificate-errors --disable-application-cache --host-resolver-rules="MAP * 192.168.100.1, EXCLUDE localhost" --disk-cache-size=0 about:blank &> /dev/null &
    else
        $browser --enable-benchmarking --enable-net-benchmarking --remote-debugging-port=9222 --user-data-dir=$profile_dir --ignore-certificate-errors --disable-application-cache --host-resolver-rules="MAP * 192.168.100.1, EXCLUDE localhost" --disk-cache-size=0 about:blank &> /dev/null &
    fi
    sleep 4
}


# Start browser
start-browser $browser $profile_dir $hostname $with_gui $web_protocol

# Create folder where we save HAR-files
har_folder="$netem_folder/logs/hars/$identifier"
mkdir -p $har_folder


# Enter URLS
while read url <&9
do
    har_filename="$har_folder/$url.har"

    if [ "$debug_mode" = true ]; then
        echo "Press enter to continue..."
        read
    fi

    echo "Fetching $url..."
    if [ "$proto_quic" = true ]; then
        chrome-har-capturer -o $har_filename "https://$hostname/files/$url"
    else
        chrome-har-capturer -o $har_filename "https://$hostname/$url"
    fi
    # If chrome-har-capturer fails we can't connect to browser
    if [ $? -ne 0 ]; then
        killall $browser
        start-browser $browser $profile_dir $hostname $with_gui $protocol
    fi

done 9< $this_folder/../config/urls.txt


