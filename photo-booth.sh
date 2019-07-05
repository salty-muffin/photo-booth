#!/bin/bash

SHUTTER=25
HALT=26
RLED=23
GLED=24

# Initialize GPIO states
gpio -g mode  $SHUTTER up
gpio -g mode  $HALT    up
gpio -g mode  $RLED    out
gpio -g mode  $GLED    out

# Flash red LED on startup to indicate ready state
for i in `seq 1 5`;
do
	gpio -g write $RLED 1
	sleep 0.2
	gpio -g write $RLED 0
	sleep 0.2
done

# turn green LED on
gpio -g write $GLED 1

while :
do
	# Check for shutter button
	if [ $(gpio -g read $SHUTTER) -eq 0 ]; then
    # debounce
    sleep 0.1
    # Wait for user to release button before resuming
		while [ $(gpio -g read $SHUTTER) -eq 0 ]; do continue; done

    # flash red LED for timer sequence
    for i in `seq 1 5`;
    do
    	gpio -g write $RLED 1
    	sleep 0.2
    	gpio -g write $RLED 0
    	sleep 0.8
    done
    gpio -g write $RLED 1
    sleep 1
    gpio -g write $RLED 0

    # shoot and print
    echo "Gorgeous!" | lp
    sleep 0.2
		raspistill -n -t 200 -w 512 -h 384 -o - | lp
    sleep 3
    for i in `seq 1 5`;
    do
      echo " " | lp
      sleep 0.2
    done

    # wait for printing
		sleep 5
	fi

	# Check for halt button
	if [ $(gpio -g read $HALT) -eq 0 ]; then
		# Must be held for 2+ seconds before shutdown is run...
		starttime=$(date +%s)
		while [ $(gpio -g read $HALT) -eq 0 ]; do
			if [ $(($(date +%s)-starttime)) -ge 2 ]; then
        gpio -g write $RLED 1
				gpio -g write $GLED 0
				shutdown -h now
			fi
		done
	fi
done
