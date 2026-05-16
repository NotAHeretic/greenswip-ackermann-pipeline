#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge
import cv2
import numpy as np

class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')
        self.bridge = CvBridge()
        self.sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_cb, 10)
        self.pub = self.create_publisher(
            Float32MultiArray, '/target_detection', 10)
        self.debug_pub = self.create_publisher(
            Image, '/camera/debug', 10)
        self.prev_found = False
        self.get_logger().info('Perception node started')

    def image_cb(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 50, 80])
        upper_red = np.array([3, 180, 135])
        mask = cv2.inRange(hsv, lower_red, upper_red)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        out = Float32MultiArray()
        img_w = float(frame.shape[1])

        if contours:
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)
            if area > 100:
                x, y, w, h = cv2.boundingRect(largest)
                cx = float(x + w / 2)
                cy = float(y + h / 2)
                out.data = [cx, cy, area, img_w, 1.0]
                if not self.prev_found:
                    self.get_logger().info(f'Box detected at cx={int(cx)} area={int(area)}')
                    self.prev_found = True
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.circle(frame, (int(cx), int(cy)), 5, (0, 255, 0), -1)
            else:
                out.data = [0.0, 0.0, 0.0, img_w, 0.0]
                self.prev_found = False
        else:
            out.data = [0.0, 0.0, 0.0, img_w, 0.0]
            if self.prev_found:
                self.get_logger().info('Box lost')
            self.prev_found = False

        self.pub.publish(out)
        debug_msg = self.bridge.cv2_to_imgmsg(frame, 'bgr8')
        self.debug_pub.publish(debug_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
