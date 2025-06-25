FROM osrf/ros:humble-desktop
# Install dependencies

# install ros package
RUN apt-get update && apt-get install -y \
      ros-${ROS_DISTRO}-demo-nodes-cpp \
      ros-${ROS_DISTRO}-demo-nodes-py && \
    rm -rf /var/lib/apt/lists/*

# Install camera module
# libcamera
RUN apt install libcamera-tools libcamera-apps-lite -y
RUN apt install libcap-dev libcamera-dev -y
RUN apt install libatlas-base-dev libopenjp2-7 libkms++-dev libfmt-dev libdrm-dev -y
RUN pip install rpi-libcamera rpi-kms
RUN apt install -y python3-picamera2 --no-install-recommends
RUN pip install picamera2
