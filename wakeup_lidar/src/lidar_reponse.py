#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan



def callback(data):

    laser_scan_msgs = data.ranges

    is_in_range = [0.1 <= x <= 1.0 for x in laser_scan_msgs]

    count_in_range = sum(is_in_range)

    if count_in_range == 0:
        rospy.loginfo("No Object in One meter range")
        lidar_pub.publish(False)
        return
    
    if count_in_range > 0:
        rospy.loginfo("Object Detected  One meter range")
        lidar_pub.publish(True)
        return

if __name__ == '__main__':
    
    rospy.init_node('lidar_response', anonymous=True)
    rospy.Subscriber('/scan_filtered', LaserScan, callback)
    lidar_pub=rospy.Publisher('/wakeup_lidar', Bool, queue_size=1)
    rospy.spin()