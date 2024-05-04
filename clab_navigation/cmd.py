#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def cmd_vel_callback(msg):
    # Callback function to receive messages from dynamixel_workbench/cmd_vel topic
    global pub
    pub.publish(msg)

if __name__ == '__main__':
    # Initialize the ROS node
    rospy.init_node('cmd_vel_republisher')

    # Subscribe to the dynamixel_workbench/cmd_vel topic
    rospy.Subscriber('/dynamixel_workbench/cmd_vel', Twist, cmd_vel_callback)

    # Create a publisher for the cmd_vel topic
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    # Spin the node
    rospy.spin()

