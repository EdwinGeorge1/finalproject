#!/usr/bin/env python
import time
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import rospy
import pygame
pygame.init()
pygame.mixer.init()

def jointStateCallback(dur,name):


    traj = [-2.5, -1.7]
    exec_time = time.time()
    pub = rospy.Publisher('/hand/joint_trajectory', JointTrajectory, queue_size = 0)

    pygame.mixer.music.load('/home/jetson/clab_ws/src/clab/audios/'+ name +'.mp3')
    pygame.mixer.music.play()


    while not rospy.is_shutdown() and time.time() - exec_time < dur:

        for pos in traj:

            joints_str = JointTrajectory()
            joints_str.joint_names=["hand_joint"]
            point = JointTrajectoryPoint()
            point.positions = [pos] 
            point.time_from_start = rospy.Duration.from_sec(0.5) 
            joints_str.points.append(point)
            time.sleep(0.5)
            pub.publish(joints_str)
            rospy.loginfo(f'command received: {joints_str}\n')
            print("done")
            # if exec_time == 

    # return        

if __name__ == '__main__':
    rospy.init_node('hand_movement', anonymous=True)
    jointStateCallback(8, "hello")