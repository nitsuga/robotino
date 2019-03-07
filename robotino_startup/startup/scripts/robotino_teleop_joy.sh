#!/bin/bash

# might want to change fixed username to something else later
ENV_LOCATION=/home/robotino/.bashrc
source ${ENV_LOCATION}

roslaunch robotino_teleop joystick_teleop.launch

bash -i

