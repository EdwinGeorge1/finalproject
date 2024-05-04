#!/bin/bash

#starting controllers and bringup
sleep 4
usr/bin/tmux -2 new-session -d -s wheel_controllers
usr/bin/tmux send-keys -t wheel_controllers.0 "roslaunch dynamixel_workbench_controllers wheels.launch" ENTER

sleep 5
usr/bin/tmux -2 new-session -d -s hand_controllers
usr/bin/tmux send-keys -t hand_controllers.0 "roslaunch dynamixel_workbench_controllers hand.launch" ENTER

sleep 5
usr/bin/tmux -2 new-session -d -s head_controllers
usr/bin/tmux send-keys -t head_controllers.0 "roslaunch dynamixel_workbench_controllers head.launch" ENTER

sleep 5
/usr/bin/tmux -2 new-session -d -s web
/usr/bin/tmux send-keys -t web.0 "roslaunch clab_bringup web.launch" ENTER

sleep 5
usr/bin/tmux -2 new-session -d -s bringup
usr/bin/tmux send-keys -t bringup.0 "roslaunch clab_bringup clab.launch" ENTER

sleep 8
usr/bin/tmux -2 new-session -d -s brave
usr/bin/tmux send-keys -t brave.0 "brave-browser --kiosk http://localhost/clab/start.php" ENTER


