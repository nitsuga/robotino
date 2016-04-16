#!/usr/bin/env python2

import rospy
import tf
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from nav_msgs.msg import OccupancyGrid

import sys
import numpy as np
import png
import random
import io

map_frame = "/map"
link_frame = "/base_link"


def pubGoal(x, y, th):
    ps = PoseStamped()
    ps.header.seq = 1
    ps.header.stamp = rospy.Time.now()
    ps.header.frame_id = "map"
    ps.pose.position.x = float(x)
    ps.pose.position.y = float(y)
    ps.pose.position.z = 0.0

    quat = tf.transformations.quaternion_from_euler(0.0, 0.0, th)
    ps.pose.orientation.x = quat[0]
    ps.pose.orientation.y = quat[1]
    ps.pose.orientation.z = quat[2]
    ps.pose.orientation.w = quat[3]

    pubGoalPose.publish(ps)


def callbackGoal(data):
    rospy.loginfo(
        "RELAY (" +
        str(data.x) +
        "; " +
        str(data.y) +
        "; " +
        str(data.z) +
        ")"
    )
    pubGoal(data.x, data.y, data.z)


def callbackMap(data):
    rospy.loginfo("RELAY recieved map")
    na = np.array(data.data)
    p = np.reshape(na, (data.info.height, data.info.width), 'C')

    # rand = str(random.randrange(0, 999999))
    # path = '/tmp/' + rand + '.png'
    # f = open(path, 'wb')
    f = io.BytesIO()
    w = png.Writer(data.info.width, data.info.height, greyscale=True)
    w.write(f, (p / 100 + 1) * 100)

    # rospy.loginfo("RELAY map saved to " + path)

    pnghex = ''.join(["%02X" % ord(x) for x in f.getvalue()]).strip()

    f.close()

    rospy.loginfo("hex length: " + str(len(pnghex)))
    # rospy.loginfo(pnghex)


if __name__ == '__main__':
    rospy.init_node('relay', anonymous=True)
    rospy.loginfo("RELAY init")

    rospy.Subscriber("logistics_goal", Point, callbackGoal)
    rospy.Subscriber("map", OccupancyGrid, callbackMap)
    pubGoalPose = rospy.Publisher(
        'move_base_simple/goal', PoseStamped, queue_size=10)
    pubCurrentPose = rospy.Publisher(
        'logistics_pose', Point, queue_size=10)

    rate = rospy.Rate(1)
    listener = tf.TransformListener()

    rospy.loginfo("waiting for tf ..")

    while not rospy.is_shutdown():
        try:
            (position, quaternion) = listener.lookupTransform(link_frame, map_frame, rospy.Time(0))

            p = Point()
            p.x = position[0]
            p.y = position[1]
            p.z = tf.transformations.euler_from_quaternion(quaternion)[2]

            rospy.loginfo("RELAY pose " + str(p))

            pubCurrentPose.publish(p)
            
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.logwarn("tf error")
            continue       

        # while(
        #     (
        #         (not listener.frameExists(map_frame)) or
        #         (not listener.frameExists(link_frame))
        #     ) and
        #     (not rospy.is_shutdown())
        # ):
        #     # rospy.loginfo("RELAY waiting for position")
        #     rate.sleep()
        #     if rospy.is_shutdown():
        #         sys.exit()

        # rospy.loginfo("tf pose available")

        # t = listener.getLatestCommonTime(link_frame, map_frame)
        # position, quaternion = listener.lookupTransform(
        #     link_frame, map_frame, t)

        rate.sleep()
