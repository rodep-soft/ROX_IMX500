FROM osrf/ros:humble-desktop

# Set up a ROS 2 workspace
WORKDIR /ros_ws

# Install dependencies
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-ros-base \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-vcstool \
    python3-pip \
    libcamera-tools \
    libcamera-apps-lite \
    libcap-dev \
    libcamera-dev \
    libatlas-base-dev \
    libopenjp2-7 \
    libkms++-dev \
    libfmt-dev \
    libdrm-dev \
    python3-opencv \
    ros-${ROS_DISTRO}-cv-bridge && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install rpi-libcamera rpi-kms picamera2

# Copy project files
COPY . /ros_ws/src/ROX_IMX500

# Build the ROS 2 workspace
RUN /bin/bash -c ". /opt/ros/${ROS_DISTRO}/setup.bash && colcon build --packages-select imx500_publisher"

# Source the ROS 2 setup file and run the publisher node
ENTRYPOINT ["/bin/bash", "-c"]
CMD [". /opt/ros/${ROS_DISTRO}/setup.bash && . /ros_ws/install/setup.bash && ros2 run imx500_publisher imx500_publisher"]
