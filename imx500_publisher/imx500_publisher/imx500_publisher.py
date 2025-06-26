import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from multiprocessing import shared_memory
import numpy as np
import cv2
import fcntl
import os

# Define lock file path
LOCK_FILE = '/tmp/imx_mem.lock'


class IMU500Publisher(Node):

    def __init__(self):
        super().__init__('imx500_publisher')
        self.publisher_ = self.create_publisher(Image, 'image_raw', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.bridge = CvBridge()
        self.shm_img = shared_memory.SharedMemory(name="imx_mem")
        self.size = np.prod((480, 640, 3))
        self.img_arr = np.ndarray((480, 640, 3), dtype=np.uint8, buffer=self.shm_img.buf)
        
        # Open lock file
        self.lock_fd = open(LOCK_FILE, 'r')
        
        self.get_logger().info('IMX500 Publisher Node has been started.')

    def timer_callback(self):
        try:
            # Acquire shared lock before reading
            fcntl.flock(self.lock_fd, fcntl.LOCK_SH)
            frame = self.img_arr.copy()
            fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
            
            # Convert BGR to RGB if necessary, depending on camera_sender.py output
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            
            # Create Image message
            img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            img_msg.header.stamp = self.get_clock().now().to_msg()
            img_msg.header.frame_id = 'camera_frame'
            
            self.publisher_.publish(img_msg)
            self.get_logger().info('Publishing image frame')
        except Exception as e:
            self.get_logger().error(f"Error publishing image: {e}")
    
    def destroy_node(self):
        self.shm_img.close()
        self.lock_fd.close()
        super().destroy_node()