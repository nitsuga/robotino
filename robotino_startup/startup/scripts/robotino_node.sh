#!/bin/bash

# might want to change fixed username to something else later
ENV_LOCATION=/home/robotino/.bashrc
source ${ENV_LOCATION}

roslaunch robotino_node robotino_node.launch

bash -i

