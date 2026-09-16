#!/usr/bin/env python3
"""Sine-sweep two left-arm joints to prove the Isaac ROS 2 bridge round-trips.

Run in a second terminal while Isaac Sim is open, the stage is loaded, and the
timeline is PLAYING:

    ./scripts/run_probe.sh

Subscribes to the joint states Isaac publishes and commands a slow sine on two
arm joints. The subscriber node in the USD ActionGraph matches joints by name,
so a partial command is fine.
"""

import math

import rclpy
from sensor_msgs.msg import JointState

STATE_TOPIC = "/isaacsim/North_Poc2_2_V3_1_joint_states"
ACTION_TOPIC = "/isaacsim/North_Poc2_2_V3_1_joint_actions"

JOINTS = ["left_arm_joint_1", "left_arm_joint_2"]
AMPLITUDES = [0.5, 0.3]
RATE_HZ = 20.0


def main() -> None:
    rclpy.init()
    node = rclpy.create_node("origami_probe")
    pub = node.create_publisher(JointState, ACTION_TOPIC, 10)

    seen = {"n": 0}

    def on_state(msg: JointState) -> None:
        seen["n"] += 1
        if seen["n"] == 1:
            node.get_logger().info(f"receiving joint states: {len(msg.name)} joints")

    node.create_subscription(JointState, STATE_TOPIC, on_state, 10)

    t = 0.0
    dt = 1.0 / RATE_HZ

    def tick() -> None:
        nonlocal t
        t += dt
        msg = JointState()
        msg.header.stamp = node.get_clock().now().to_msg()
        msg.name = JOINTS
        msg.position = [a * math.sin(t) for a in AMPLITUDES]
        pub.publish(msg)

    node.create_timer(dt, tick)
    node.get_logger().info(f"commanding {JOINTS} on {ACTION_TOPIC} -- Ctrl+C to stop")

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
