#!/bin/bash
/usr/bin/tmux -2 new-session -d -s video
/usr/bin/tmux send-keys -t video.0 "feh -F -N /home/jetson/clab_ws/src/clab/clab_ui/gif/$1" ENTER