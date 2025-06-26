from picamera2.picamera2 import *
import numpy as np
import time
from multiprocessing import shared_memory
import fcntl
import os

# Define lock file path
LOCK_FILE = '/tmp/imx_mem.lock'

picamera = Picamera2()
preview_config = picamera.create_preview_configuration()
preview_config["main"]["size"] = (640, 480)
picamera.configure(preview_config)
picamera.start()
time.sleep(1)

size = np.prod((480, 640, 3))
shm_img = shared_memory.SharedMemory(name="imx_mem", create=True, size=size)
img_arr = np.ndarray((480, 640, 3), dtype=np.uint8, buffer=shm_img.buf)

# Open lock file
lock_fd = open(LOCK_FILE, 'w')

try :
    while True:
        frame = picamera.capture_array("main")
        frame = frame[:, :, :3]
        
        # Acquire exclusive lock before writing
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        img_arr[:] = frame
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        
        time.sleep(0.01)
except KeyboardInterrupt:
    print("KeyboardInterrupt received, stopping camera capture.")
finally :
    shm_img.close()
    shm_img.unlink()
    lock_fd.close()
    os.remove(LOCK_FILE)

frame = picamera.capture_array("main")