# ROS2 Visual Servoing — Ackermann Robot
## Perception-to-Action Pipeline for Ackermann Mobile Robot

---

## Overview

This project implements a complete ROS 2 perception-to-action pipeline for an Ackermann-steered mobile robot in Gazebo (Ignition / gz sim).

The robot uses a front-mounted camera to detect a red box (target object) using OpenCV and navigates toward it while respecting Ackermann kinematic constraints (no in-place rotation).

The system is fully dynamic and works across multiple object arrangements without any hardcoded positions.

---

## Key Features

- ROS 2 + Gazebo simulation setup from a minimal URDF
- Camera integration and ROS–Gazebo bridging
- OpenCV-based perception:
  - HSV color masking
  - Contour detection
  - Centroid extraction
- Control system:
  - Visual error to steering angle mapping
  - Ackermann-compliant motion (no spinning in place)
  - Speed modulation based on steering
- Dynamic robustness:
  - Works across multiple shuffled arrangements
  - No dependency on fixed world coordinates

---

## System Architecture

### Perception Node
- Subscribes to camera image topic
- Applies HSV masking to isolate the red target
- Extracts contour and computes centroid
- Publishes horizontal error
- Subscribes to camera topic (configured via ROS–Gazebo bridge)

### Control Node
- Subscribes to perception output
- Converts error into steering command
- Maintains forward motion at all times
- Reduces speed at higher steering angles
- Publishes velocity and steering commands compatible with Ackermann motion

### Simulation
- Gazebo world includes:
  - Target: Box
  - Decoys: Sphere, Capsule, Cylinder
- Robot spawned using ros_gz_sim
- ROS–Gazebo communication handled via ros_gz_bridge

---

## Workspace Structure

```
ackermann_ws/
├── src/
│   └── ackermann_pipeline/
│       ├── config/
│       │   └── bridge.yaml
│       ├── ackermann_pipeline/
│       │   ├── perception_node.py
│       │   └── control_node.py
│       ├── launch/
│       │   └── simulation.launch.py
│       ├── scripts/
│       │   └── swap.sh
│       ├── urdf/
│       │   ├── robot.urdf
│       │   └── ack_urdf.xacro
│       ├── worlds/
│       │   └── shapes.sdf
│       ├── package.xml
│       ├── setup.py
│       └── setup.cfg
├── README.md
└── .gitignore
```

---

## Dependencies

- ROS 2 (Jazzy or compatible)
- Gazebo (gz sim / Ignition)
- OpenCV (Python)
- ros_gz_bridge
- cv_bridge

---

## Build Instructions

```bash
cd ~/ackermann_ws
colcon build
source install/setup.bash
```

---

## Run Simulation

```bash
ros2 launch ackermann_pipeline simulation.launch.py
```

This will:
- Launch Gazebo with the world
- Spawn the robot
- Start ROS–Gazebo bridge
- Start perception node
- Start control node

---

## Arrangement Switching (Robustness Testing)

To test different object arrangements during runtime:

```bash
cd ~/ackermann_ws/src/ackermann_pipeline
./scripts/swap.sh
```

Then select:

```
1 → Target swaps with sphere
2 → Target swaps with capsule
3 → Target swaps with cylinder
```

This uses Gazebo services (`/world/.../set_pose`) to dynamically reposition objects.

---

## Kinematic Constraints

The control logic strictly follows Ackermann steering:

- No in-place rotation
- Continuous forward motion
- Turning achieved via steering angle
- Speed reduced during sharp turns

Differential-drive behavior is not used.

---

## Assumptions

- Target is identified using color (red box)
- Camera topics and bridge configuration are defined manually
- Navigation is purely vision-driven (no map or global coordinates)

---

## Verification

After launching:

- The robot detects the red box using camera input
- It continuously moves forward and steers toward the target
- It does not rotate in place
- It successfully reaches the target across multiple arrangements

---

## Author

Abhijit Mahadik
