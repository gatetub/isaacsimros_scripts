#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import time


class JointMover(Node):
    def __init__(self):
        super().__init__('joint_mover')
        self.pub = self.create_publisher(JointState, '/joint_states', 10)
        time.sleep(1)

        self.joint_names = [
            'lower_body_joint_1', 'lower_body_joint_2',
            'lower_body_joint_3', 'lower_body_joint_4',
            'lower_body_joint_5',
            'left_arm_joint_1', 'left_arm_joint_2', 'left_arm_joint_3',
            'left_arm_joint_4', 'left_arm_joint_5', 'left_arm_joint_6',
            'left_arm_joint_7',
            'left_thumb_CMC_FE', 'left_thumb_CMC_AA',
            'left_thumb_MCP_FE', 'left_thumb_MCP_AA', 'left_thumb_IP',
            'left_index_MCP_FE', 'left_index_MCP_AA',
            'left_index_PIP', 'left_index_DIP',
            'left_middle_MCP_FE', 'left_middle_MCP_AA',
            'left_middle_PIP', 'left_middle_DIP',
            'left_ring_MCP_FE', 'left_ring_MCP_AA',
            'left_ring_PIP', 'left_ring_DIP',
            'left_pinky_CMC', 'left_pinky_MCP_FE', 'left_pinky_MCP_AA',
            'left_pinky_PIP', 'left_pinky_DIP',
            'right_arm_joint_1', 'right_arm_joint_2', 'right_arm_joint_3',
            'right_arm_joint_4', 'right_arm_joint_5', 'right_arm_joint_6',
            'right_arm_joint_7',
            'right_thumb_CMC_FE', 'right_thumb_CMC_AA',
            'right_thumb_MCP_FE', 'right_thumb_MCP_AA', 'right_thumb_IP',
            'right_index_MCP_FE', 'right_index_MCP_AA',
            'right_index_PIP', 'right_index_DIP',
            'right_middle_MCP_FE', 'right_middle_MCP_AA',
            'right_middle_PIP', 'right_middle_DIP',
            'right_ring_MCP_FE', 'right_ring_MCP_AA',
            'right_ring_PIP', 'right_ring_DIP',
            'right_pinky_CMC', 'right_pinky_MCP_FE', 'right_pinky_MCP_AA',
            'right_pinky_PIP', 'right_pinky_DIP',
            'neck_joint_1', 'neck_joint_2',
        ]
        self.num_joints = len(self.joint_names)

    def publish_pose(self, positions):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = [float(p) for p in positions]
        msg.velocity = []
        msg.effort = []
        self.pub.publish(msg)

    def run(self, hz=20):
        dt = 1.0 / hz
        t = 0.0
        self.get_logger().info('Running sine wave demo (Ctrl+C to stop)...')
        while rclpy.ok():
            t += dt
            positions = []
            for j in range(self.num_joints):
                freq = 0.5 + j * 0.1
                amp = 0.3
                positions.append(amp * math.sin(2.0 * math.pi * freq * t))
            self.publish_pose(positions)
            time.sleep(dt)


def main():
    rclpy.init()
    node = JointMover()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.publish_pose([0.0] * node.num_joints)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
