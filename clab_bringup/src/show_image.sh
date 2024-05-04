#!/bin/bash
/usr/bin/tmux -2 new-session -d -s image
/usr/bin/tmux send-keys -t image.0 "eog -f /home/jetson/clab_ws/src/clab/Images/$1" ENTER
#/usr/bin/tmux send-keys -t image.0 "eog -f /home/asimov/IRA_V2_ws/src/qr.png" ENTER
sleep 1




