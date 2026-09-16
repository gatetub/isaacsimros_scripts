#!/bin/bash
source /opt/ros/jazzy/setup.sh
source /ros2_ws/install/setup.bash

ros2 launch NTH_POC2_2_URDF_20251119v1 display.launch.py &
LAUNCH_PID=$!

sleep 3

python3 /root/joint_mover.py

wait $LAUNCH_PID
