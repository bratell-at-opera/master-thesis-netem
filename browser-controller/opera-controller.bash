#!/bin/bash
set -e

opera_windows=$(xdotool search --sync --onlyvisible --name " \- Opera")

# Ugly hack to remove windows which are not Opera
# ---------------------------------------------
# Operas slack has title "Slack - Opera"
other_windows="$(xdotool search --name 'Slack')"
# Author has Opera in hostname which are in terminals
other_windows="$other_windows $(xdotool search --name $(hostname))"

opera_window=""
for window in $opera_windows
do
    in_other_windows=false
    for other_window in $other_windows
    do
        if [ "$window" = "$other_window" ]; then
            in_other_windows=true
            break
        fi
    done
    if [ "$in_other_windows" = false ]; then
        opera_window=$window
        break
    fi
done

if [ -z "$opera_window" ]; then
    echo "ERROR: Can not find Opera window!"
    exit 2
fi

# End of ugly hack ---------------------

if [ "$1" = "--setup" ]; then
    # Bring Opera to front
    xdotool windowactivate $opera_window
    # Set window size for proportions to be correct
    xdotool windowsize $opera_window 1920 1100
    # open dev-tools
    xdotool key --clearmodifiers "Ctrl+Shift_L+i"
    # Activate network tab
    sleep 2
    xdotool mousemove --window $opera_window 1650 130 click 1
    # Disable cache
    sleep 1
    xdotool mousemove --window $opera_window 1710 150 click 1

elif [ "$1" = "--save-stats" ] && [ "$#" -eq 2 ]; then
    directory="$2"
    # Bring Opera to front
    xdotool windowactivate $opera_window
    sleep 1
    # Open save dialog
    xdotool mousemove --window $opera_window 1710 550 click 3
    sleep 1
    xdotool mousemove --window $opera_window 1720 600 click 1
    sleep 1
    # Type in the appropriate filename
    xdotool key --delay 20 --clearmodifiers "Home"
    xdotool type --delay 10 --clearmodifiers "${directory}/"
    xdotool key --delay 20 --clearmodifiers "Return"

    # Wait for the file to be completely saved
    sleep 3
else
    echo "ERROR: Incorrect usage!"
    exit 1
fi
