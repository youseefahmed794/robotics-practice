# Robotics Practice

Python and ROS 2 learning exercises by Youseef Abdel Tawwab, a Mechatronics Engineering graduate building practical autonomous robotics skills.

## Current scope

This repository contains a small distance-based decision function and a ROS 2 subscriber that uses it. It is an early learning project toward an Autonomous Mobile Robot.

The node logs a decision; it does not publish velocity commands, control motors, or implement autonomous navigation. Distances are supplied manually in the example below, not read from a physical sensor.

## Implemented behavior

| Distance in meters | Decision |
| --- | --- |
| Below 0.5 | `STOP` |
| 0.5 up to, but excluding, 1.0 | `SLOW` |
| 1.0 or above | `GO` |

`distance_listener` subscribes to `/distance` using `std_msgs/msg/Float64` and logs the received distance and decision.

## Repository structure

- `motion_decision.py`: standalone Python exercise.
- `ros2_ws/src/motion_control/`: ROS 2 Python package.
- `ros2_ws/src/motion_control/motion_control/motion_decision.py`: decision logic used by the node.
- `ros2_ws/src/motion_control/motion_control/distance_listener.py`: ROS 2 subscriber.
- `ros2_ws/src/motion_control/test/`: generated style and copyright checks; these are not decision-behavior tests.

## Run the standalone exercise

Requires Python 3. From the repository root:

```bash
python3 motion_decision.py
```

Enter a distance in meters when prompted.

## Build and run the ROS 2 package

Prerequisites: a compatible Ubuntu/ROS 2 installation with `rclpy`, `std_msgs`, and `colcon`. The specific supported OS and ROS 2 distribution are not yet documented here.

The commands below are instructions derived from the source; the complete ROS 2 workflow was not executed during the documentation review. Replace `<your_distro>` with your installed distribution name.

Terminal 1:

```bash
source /opt/ros/<your_distro>/setup.bash
cd ~/robotics_practice/ros2_ws
colcon build --packages-select motion_control
source install/setup.bash
ros2 run motion_control distance_listener
```

The path assumes your clone is at `~/robotics_practice`; adjust it to your actual directory.

Terminal 2, with the same ROS 2 environment:

```bash
source /opt/ros/<your_distro>/setup.bash
ros2 topic pub --once /distance std_msgs/msg/Float64 '{data: 0.3}'
ros2 topic pub --once /distance std_msgs/msg/Float64 '{data: 0.7}'
ros2 topic pub --once /distance std_msgs/msg/Float64 '{data: 1.5}'
```

Expected decisions in Terminal 1: `STOP`, `SLOW`, and `GO`, respectively. These are expected outputs, not a recorded integration-test result. Stop the listener with Ctrl+C.

## Verification

On 2026-10-18, the packaged Python function at source commit `1b5d9aa` was imported and checked with six assertions in a separate review environment:

| Input | Expected | Result |
| --- | --- | --- |
| 0 | STOP | Passed |
| 0.49 | STOP | Passed |
| 0.5 | SLOW | Passed |
| 0.99 | SLOW | Passed |
| 1.0 | GO | Passed |
| 2.0 | GO | Passed |

To reproduce these checks from the repository root:

```bash
PYTHONPATH=ros2_ws/src/motion_control python3 - <<'PY'
from motion_control.motion_decision import decide_motion

cases = [(0, 'STOP'), (0.49, 'STOP'), (0.5, 'SLOW'),
         (0.99, 'SLOW'), (1.0, 'GO'), (2.0, 'GO')]
for distance, expected in cases:
    actual = decide_motion(distance)
    assert actual == expected, (distance, actual, expected)
print('6 decision checks passed')
PY
```

ROS 2 integration, package build, and the existing style checks were not run in that environment because `rclpy` was unavailable. The six checks validate only the decision function for the listed inputs.

## Known limitations and next steps

- Input validation for negative distances, NaN, and infinity is not implemented.
- The standalone and packaged decision functions are currently duplicated.
- Package metadata still contains placeholder descriptions.
- Add maintained automated behavior tests and record a ROS 2 execution demo.
- Simulation, sensor integration, and navigation are future work, not completed features of this repository.
