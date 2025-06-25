from picamera2.picamera2 import *
import numpy as np
import time
from multiprocessing import shared_memory
import cv2

shm_img = shared_memory.SharedMemory(name="imx_mem")
size = np.prod((480, 640, 3))
img_arr = np.ndarray((480, 640, 3), dtype=np.uint8, buffer=shm_img.buf)
while True:
    try:
        frame = img_arr.copy()
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting camera display.")
            break
        time.sleep(0.01)  # Sleep to reduce CPU usage
    except KeyboardInterrupt:
        print("KeyboardInterrupt received, stopping camera display.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break

cv2.destroyAllWindows()