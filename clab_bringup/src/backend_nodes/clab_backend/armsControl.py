#! /usr/bin/env python

import rospy
import time
import threading
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class armsControl:
    '''
    usage: 

    ### ALWAYS INIT ROS NODE BEFORE CREATING CLASS OBJECT

    * `start()` - runs till obj goes out of scope.
    * `start(x)` - runs for x seconds.
    * `stop()` - will stop motion at any point of time.  

    Author: Arthur 
    Date: 16/2/23
    Description: controlling arms motion of clab robot
    '''
    NUM_POINTS = 3 # number of points in the trajectory message
    FREQ = 10 # frequency of the trajectory publisher, in Hz
    
    def __init__(self, 
                limits = (0.8, 1.8), 
                topic = "/hand/joint_trajectory",
                joint = "hand_joint",
                time_step = 0.5):

        self.STOP = False
        self.RUN = False
        self.time_step = time_step
        self.arms_msg, self.stop_msg = self.createArmsTraj(limits, joint)

        self.arms_pub = rospy.Publisher(topic, JointTrajectory, queue_size=1)
        self.rate = rospy.Rate(armsControl.FREQ)

        if self.arms_pub.get_num_connections() == 0:
            rospy.logwarn("arms controller not subscribed to " + topic)
        while self.arms_pub.get_num_connections() == 0:
            pass
        rospy.loginfo("ARMS Control ready. Subscriber connected")

    def __del__(self):

        self.STOP = True

    def createPoint(self, positions, seconds_from_start):
        point = JointTrajectoryPoint()
        point.positions = positions[:]
        point.time_from_start = rospy.Duration.from_sec(seconds_from_start)
        return point

    def createArmsTraj(self, limits, joint):

        msg = JointTrajectory()
        stop_msg = JointTrajectory()

        msg.joint_names.append(joint)
        stop_msg.joint_names.append(joint)

        start_point = self.createPoint([limits[0]], 0)

        msg.points.append(start_point)
        stop_msg.points.append(start_point)

        count = 1
        while count < armsControl.NUM_POINTS:

            mid_point = self.createPoint([limits[1]], self.time_step*count)
            end_point = self.createPoint([limits[0]], self.time_step*(count+1))

            msg.points.append(mid_point)
            msg.points.append(end_point)
           
            count = count + 2           

        return msg, stop_msg

    def armsGesture(self, duration = None):
        
        while(self.arms_pub.get_num_connections() <= 0):
            pass
        rospy.loginfo("starting ARMS gesture")

        if duration != None and duration > 0:

            start_time = time.time()
            while not rospy.is_shutdown() and not self.STOP and time.time() - start_time < duration:
                self.arms_pub.publish(self.arms_msg)
                self.rate.sleep()
            
            if not self.STOP:
                rospy.loginfo("gesture timeout. stopping ARMS")

        else:

            while not rospy.is_shutdown() and not self.STOP:
                self.arms_pub.publish(self.arms_msg)
                self.rate.sleep()

        self.STOP = False
        self.RUN = False
          
    def start(self, duration = None):

        if not self.STOP and self.RUN:
            rospy.logwarn("new thread started without closing previous. stopping old thread")
            self.stop() # stop thread and start new one if start is called twice
        
        if self.STOP and self.RUN:
            rospy.logwarn("waiting for thread to close")
            time.sleep(armsControl.NUM_POINTS/armsControl.FREQ) # wait for the previous motion to finish
        
        arms_thread = threading.Thread(target=self.armsGesture, args=(duration,))
        arms_thread.start()
        self.RUN = True

    def stop(self):

        rospy.loginfo("stopping ARMS gesture")
        self.STOP = True

    def hand_standby(self, pos):

        standby_msg = JointTrajectory()

        standby_msg.joint_names.append("hand_joint")

        pub_time_cnt = 0

        while pub_time_cnt <= 1 :

            point = JointTrajectoryPoint()
            point.positions = [pos]
            point.time_from_start = rospy.Duration.from_sec(0.5)
            standby_msg.points.append(point)
            
            self.arms_pub.publish(standby_msg)
            pub_time_cnt = pub_time_cnt + 1

          

if __name__ == "__main__":

    rospy.init_node("test")
    obj = armsControl()

    obj.start()
    # time.sleep(15)
    # obj.stop()



