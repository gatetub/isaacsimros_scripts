# Source this to use Isaac Sim 4.5's bundled ROS 2 Humble libraries.
# There is no system ROS 2 on this host, so this stands in for
# `source /opt/ros/humble/setup.bash`.

export ISAAC_SIM=/media/avishikta/data/4.5-sim/isaac-sim-standalone-4.5.0-linux-x86_64
export ROS_BRIDGE=$ISAAC_SIM/exts/isaacsim.ros2.bridge

export ROS_DISTRO=humble
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ROS_BRIDGE/humble/lib
export PYTHONPATH=$PYTHONPATH:$ROS_BRIDGE/humble/rclpy
