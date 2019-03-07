#!/bin/bash

# might want to change fixed username to something else later
ENV_LOCATION=/home/robotino/.bashrc
source ${ENV_LOCATION}

MAPS_LOCATION=/home/robotino/ros/robotino/src/robotino/robotino-ros-pkg/robotino_navigation/maps/

# SEB15 arena map with two panels removed for MR tasks
roslaunch robotino_navigation robotino_navigation.launch map_file:=${MAPS_LOCATION}/map-strand-first-floor-5cm.yaml

bash -i

