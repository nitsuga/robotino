#!/bin/bash

# might want to change fixed username to something else later
ENV_LOCATION=/home/robotino/.bashrc
source ${ENV_LOCATION}

roscore

bash -i

