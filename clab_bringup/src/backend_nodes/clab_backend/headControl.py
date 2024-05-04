#! /usr/bin/env python

import rospy
import time
import threading
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class headControl:
    '''
    usage: 

    ### ALWAYS INIT ROS NODE BEFORE CREATING CLASS OBJECT

    #### Methods:
    * `movePoint(pos_name)`: move to a defined position.\nPositions are added in `point_dict`.
    * `startRoll(duration = None)`: start the side-to-side roll motion. \nOptional Duration.
    * `stopRoll()`: stop the motion.

    Author: Arthur 
    Date: 16/2/23
    Description: controlling head motion of clab robot
    '''
    NUM_POINTS = 4 # number of poinets in the side-to-side trajectory messages.
    FREQ = 20 # frequency of the trajectory message publisher, in Hz.
    INTERVAL = 10 # number of trajectory messages sent for every movePoint() call.
    
    def __init__(self, 
                point_dict = {'home':(0.375, -0.349),
                              'down':(0.0, 0.0),
                              "left_node:": (0.1, -0.4),
                              "right_node": (0.4, -0.1)},
                offset = 0.075,
                topic = "/head/joint_trajectory",
                joints = ["head_left_joint", "head_right_joint"],
                time_step = 0.4):

        self.STOP = False
        self.RUN = False
        self.current = [0,0]
        self.joints = joints
        self.time_step = time_step
        self.offset = offset
        self.point_dict = point_dict

        self.head_pub = rospy.Publisher(topic, JointTrajectory, queue_size=1)
        self.rate = rospy.Rate(headControl.FREQ)

        if self.head_pub.get_num_connections() == 0:
            rospy.logwarn("HEAD controller not subscribed to " + topic)
        while(self.head_pub.get_num_connections() <= 0): #wait for subscriber to come online.
            pass
        rospy.loginfo("HEAD Control ready. Subscriber Connected")

    def __del__(self):
        self.STOP = True

    def movePoint(self, pos_name):
        if self.RUN: # stop the side-to-side motion if still its running.
            self.stopRoll() 
            while self.RUN: # wait for side-to-side motion to halt. 
                pass 
            interval = headControl.INTERVAL*2 
        else:
            interval = headControl.INTERVAL

        if pos_name in self.point_dict: # check for requested position in position dictionary.
            positions = self.point_dict[pos_name] 
        else:
            rospy.logerr("given position " + pos_name + " does not exist in point dictionary. Defaulting to mid point")
            positions = self.point_dict['mid']

        point = self.createPoint(positions, self.time_step) # create Joint Trajectory point
        msg = JointTrajectory()
        msg.joint_names = self.joints[:]
        msg.points.append(point) # add created point to a trajectory message

        while(self.head_pub.get_num_connections() <= 0): # ensure that subscriber is connected
            pass
        rospy.loginfo("HEAD moving to " + str(positions))

        for i in range(interval): # publish the trajectory message repeatedly
            self.head_pub.publish(msg)
            self.rate.sleep() # ensure that frequency of publishing is maintained.

        self.current = positions[:]

    def createPoint(self, positions, seconds_from_start):
        point = JointTrajectoryPoint()
        point.positions = positions[:]
        point.time_from_start = rospy.Duration.from_sec(seconds_from_start)
        return point

    def createHeadRollTraj(self):
        head_msg = JointTrajectory()
        head_msg.joint_names = self.joints[:]
        count = 0

        while count < headControl.NUM_POINTS:

            left_point = self.createPoint([self.current[0] - self.offset, self.current[1] - self.offset], 
                                          count*self.time_step + self.time_step)
            
            right_point = self.createPoint([self.current[0] + self.offset, self.current[1] + self.offset], 
                                           count*self.time_step + 2*self.time_step)

            head_msg.points.append(left_point)
            head_msg.points.append(right_point)
            count += 2

        return head_msg

    def headRoll(self, duration = None):
        
        while(self.head_pub.get_num_connections() <= 0): #ensure subscriber is connected
            pass
        rospy.loginfo("starting HEAD roll motion")
        head_msg = self.createHeadRollTraj()

        if duration != None and duration > 0:

            start_time = time.time()
            while not rospy.is_shutdown() and not self.STOP and time.time() - start_time < duration:
                self.head_pub.publish(head_msg)
                self.rate.sleep()
            
            if not self.STOP:
                rospy.loginfo("timeout. stopping HEAD roll")

        else:

            while not rospy.is_shutdown() and not self.STOP:
                self.head_pub.publish(head_msg)
                self.rate.sleep()

        self.STOP = False
        self.RUN = False
          
    def startRoll(self, duration = None): # duration in seconds

        if not self.STOP and self.RUN:
            rospy.logwarn("new thread started without closing previous. stopping old thread")
            self.stopRoll() # stop thread and start new one if start is called twice
        
        if self.STOP and self.RUN:
            rospy.logwarn("waiting for thread to close")
            time.sleep(headControl.INTERVAL/headControl.FREQ) # wait for the previous motion to finish
        
        head_thread = threading.Thread(target=self.headRoll, args=(duration,))
        head_thread.start()
        self.RUN = True
        
    def stopRoll(self):

        rospy.loginfo("stopping HEAD gesture")
        self.STOP = True
        

if __name__ == "__main__":

    rospy.init_node("test")
    obj = headControl()
        
    obj.movePoint("home")
    obj.movePoint("down")
    # obj.startRoll()

    # input("enter to stop")
    # obj.stopRoll()
    time.sleep(1)
    obj.movePoint("home")
    obj.movePoint("down")