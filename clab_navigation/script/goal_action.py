#!/usr/bin/env python
import roslib
import rospy
import smach
import smach_ros

import actionlib
from actionlib_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import *
from geometry_msgs.msg import PoseStamped


def talker():
	rospy.init_node('goal_action_client', anonymous=True)
	move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

	goal = MoveBaseGoal()
	#rospy.logerr("Connected to move base server")
	goal.target_pose.header.frame_id = 'map'
	# Set the time stamp to "now"
	goal.target_pose.header.stamp = rospy.Time.now()
	# Set the goal there
	goal.target_pose.pose.position.x=-0.0731
	goal.target_pose.pose.position.y=0.0699
	goal.target_pose.pose.position.z=0		
	goal.target_pose.pose.orientation.x=0
	goal.target_pose.pose.orientation.y=0
	goal.target_pose.pose.orientation.z=-0.2966
	goal.target_pose.pose.orientation.w=0.9549
	print("*_*")
	move_base.send_goal(goal)
	finished_within_time = move_base.wait_for_result(rospy.Duration(1200000)) 
	state = move_base.get_state()
	print("finishe within time "+finished_within_time)
	print("state is "+state)




if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

