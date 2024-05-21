#!/usr/bin/env python
from mbf_msgs.msg import ExePathActionGoal
from mbf_msgs.msg import ExePathResult
from geometry_msgs.msg import PoseStamped
import rospy
import sys
import csv



def load_points(path):
    glob_path = ExePathActionGoal()
    no_of_points = 0
    
    with open(path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.header.seq = no_of_points
            pose.pose.position.x = float(row[0])
            pose.pose.position.y = float(row[1])
            pose.pose.position.z = float(row[2])
            pose.pose.orientation.x = float(row[3])
            pose.pose.orientation.y = float(row[4])
            pose.pose.orientation.z = float(row[5])
            pose.pose.orientation.w = float(row[6])
            glob_path.goal.path.poses.append(pose)
            no_of_points += 1
    glob_path.goal.controller = 'eband'
    glob_path.goal.path.header.frame_id = 'map'
    print("{} points are readed".format(no_of_points))
    return glob_path



if __name__ == "__main__":
    rospy.init_node('path_sender')
    
    path = sys.argv[1]
    glob_path = load_points(path)
    print(glob_path)
    pub = rospy.Publisher('move_base/exe_path/goal', ExePathActionGoal, queue_size=10)
    rospy.sleep(1)
    pub.publish(glob_path)
