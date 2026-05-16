#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist

class ControlNode(Node):
    MAX_STEER = 0.4
    WHEEL_BASE = 0.29502

    def __init__(self):
        super().__init__('control_node')
        self.sub = self.create_subscription(
            Float32MultiArray, '/target_detection', self.detection_cb, 10)
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.target_reached = False
        self.search_dir = 1.0
        self.search_count = 0
        self.log_count = 0
        self.get_logger().info('Control node started')

    def detection_cb(self, msg):
        cx, cy, area, img_w, found = msg.data
        cmd = Twist()

        if self.target_reached:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.pub.publish(cmd)
            self.log_count += 1
            if self.log_count % 30 == 0:  # log every ~1 sec
                self.get_logger().info('TARGET REACHED! Robot stopped at box.')
            return

        if not found:
            self.search_count += 1
            if self.search_count > 80:
                self.search_dir *= -1
                self.search_count = 0
            cmd.linear.x = 0.25
            cmd.angular.z = self.MAX_STEER * self.search_dir
            self.pub.publish(cmd)
            return

        error = (cx - img_w / 2.0) / (img_w / 2.0)

        if area > 30000:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.target_reached = True
            self.get_logger().info('='*50)
            self.get_logger().info('TARGET REACHED! Robot stopped at box.')
            self.get_logger().info('='*50)
            self.pub.publish(cmd)
            return

        cmd.linear.x = float(0.4 * (1.0 - 0.6 * abs(error)))
        cmd.angular.z = float(-error * self.MAX_STEER)
        self.get_logger().info(
            f'Tracking: error={error:.2f} speed={cmd.linear.x:.2f} steer={cmd.angular.z:.2f}')
        self.pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
