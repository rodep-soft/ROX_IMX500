import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from multiprocessing import shared_memory
import numpy as np


class IMU500Publisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.shm_img = shared_memory.SharedMemory(name="imx_mem")
        self.size = np.prod((480, 640, 3))
        self.img_arr = np.ndarray((480, 640, 3), dtype=np.uint8, buffer=self.shm_img.buf)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1
    
    def recieve_img(self):
        try:
            frame = self.img_arr.copy()
        except Exception as e:
            self.get_logger().error(f"Error receiving image: {e}")
        return frame


def main(args=None):
    rclpy.init(args=args)

    imu500_publisher = IMU500Publisher()

    rclpy.spin(imu500_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    imu500_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()