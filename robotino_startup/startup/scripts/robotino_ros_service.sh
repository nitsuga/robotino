#!/bin/bash

STARTUP_HOME=/home/robotino/ros/robotino/src/robotino/robotino_startup/startup

source /opt/ros/kinetic/setup.bash

# Robotino ROS workspace
source /home/robotino/ros/robotino/devel/setup.bash

start () {
echo "Sleeping for 5"
/bin/sleep 5s
echo "Starting..."
for i in roscore robotino_node robotino_teleop_joy # robotino_navigation
do
    TMUX_NAME=$i
    SCRIPT_NAME=$i
    echo "  - ${TMUX_NAME}"
    echo "tmux new -d -s ${TMUX_NAME} ${STARTUP_HOME}/scripts/${SCRIPT_NAME}.sh"
    #echo "tmux new-session -d -s ${TMUX_NAME} '${STARTUP_HOME}/scripts/tmux_run.sh ${STARTUP_HOME}/scripts/${SCRIPT_NAME}.sh'"
    #eval "tmux new-session -d -s ${TMUX_NAME} '${STARTUP_HOME}/scripts/tmux_run.sh ${STARTUP_HOME}/scripts/${SCRIPT_NAME}.sh'"
    tmux new-session -d -s ${TMUX_NAME} ${STARTUP_HOME}/scripts/${SCRIPT_NAME}.sh
    # Give graceful 5 seconds to let roscore to start
    /bin/sleep 5s
done
RETVAL=$?
echo "Done"
return $RETVAL
}

stop(){
echo "Stopping..."
for i in roscore robotino_node robotino_teleop_joy # robotino_navigation
do
    TMUX_NAME=$i
    echo "  - ${TMUX_NAME}"
    # "|| true" to ignore error exit code from tmux if the session is closed already.
    tmux send-keys -t ${TMUX_NAME} Enter C-c Enter C-d || true
    echo "      SIGTERM sent"
    /bin/sleep 3s
    tmux kill-session -t ${TMUX_NAME} || true
    echo "      Killing session"
done
RETVAL=$?
echo "Done"
return $RETVAL
}

case "$1" in
    start)
        start
    ;;
    stop)
        stop
    ;;
    *)
        echo $"Usage: script {start|stop}"
        exit 3
    ;;
esac

exit $RETVAL
