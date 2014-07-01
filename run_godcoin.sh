#!/bin/sh
SERVICE='python ./run_p2pool.py --net godcoin'

if ps ax | grep -v grep | grep "$SERVICE" > /dev/null
then
        echo "$SERVICE is already running!"
else
        screen  -m -S screengod python ./run_p2pool.py --net godcoin --give-author 0 --disable-upnp -f 1 -a GUrbSwBQPwweijNah7Zo8e5xhnhHbttc55

	wait
fi
