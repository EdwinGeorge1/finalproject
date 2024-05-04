#!/bin/bash


#closing controllers and bringup
/usr/bin/tmux send-keys -t bringup.0 "" C-c
/usr/bin/tmux send-keys -t wheel_controllers.0 "" C-c
/usr/bin/tmux send-keys -t hand_controllers.0 "" C-c
/usr/bin/tmux send-keys -t head_controllers.0 "" C-c
/usr/bin/tmux send-keys -t clab_py.0 "" C-c
sleep 5

#killing all tmux servers
/usr/bin/tmux kill-session -t bringup
/usr/bin/tmux kill-session -t clab_py
/usr/bin/tmux kill-session -t web
/usr/bin/tmux kill-session -t wheel_controllers
/usr/bin/tmux kill-session -t hand_controllers
/usr/bin/tmux kill-session -t head_controllers
sleep 10
/usr/bin/tmux kill-session -t brave

