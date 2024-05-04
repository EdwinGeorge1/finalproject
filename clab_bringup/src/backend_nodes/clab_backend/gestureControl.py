#! /usr/bin/env python

from armsControl import armsControl
from headControl import headControl

class gestureControl:
    '''
    ### ALWAYS INIT ROS NODE BEFORE CREATING CLASS INSTANCE

    #### methods:
    * `setHead(position_name)`: to position head
    * `start(duration = None)`: to start head roll and arms flapping. Optional duration of movement.
    * `stop()`: to stop head roll and arms flapping

    #### class flags:
    * `ARMS_ENABLE = True`: set to false to disable arms. 
    * `HEAD_ENABLE = True`: set to false to disable head.

    Author: Arthur 
    Date: 16/2/23
    Description: controlling head and arms motion of clab robot
    '''
    ARMS_ENABLE = True # enable/disable arms motion
    HEAD_ENABLE = True # enable/disable head motion
    
    def __init__(self,
                                                        # ARMS PARAMs
                arms_limits = (0.8, 1.8),               # (closed, open) in radians
                arms_topic = "/hand/joint_trajectory",  # topic to publish to the arms controller
                arms_joint = "hand_joint",              # name of the arms joint as per controller params 
                arms_time_step = 0.5,                   # transition period between extended and retracted, in seconds 

                                                        # HEAD PARAMS
                head_point_dict = {"home":(0.375, -0.349),
                                   "down": (0.1, -0.1),
                                   "left_nod": (0.16260196268558502, -0.5476311445236206),
                                   "right_nod": (0.5813787579536438, -0.11658254265785217)},  # set the desired head servo positions here, in radians
                                     
                head_roll_offset = 0.075,                 # half difference in angle between servos when tilted sideways in radians
                head_topic = "/head/joint_trajectory",  # topic to publish to the head controller
                head_joints = ["head_left_joint",       # name of the joints as per head controller params. 
                               "head_right_joint"],     # NOTE: the order has to be [left, right]
                head_time_step = 0.4):                 # transition period between head states, in seconds.  
 
        if gestureControl.ARMS_ENABLE:       
            self.arms = armsControl(arms_limits, arms_topic, arms_joint, arms_time_step)
        
        if gestureControl.HEAD_ENABLE: 
            self.head = headControl(head_point_dict, head_roll_offset, head_topic, head_joints, head_time_step)
          
    def start(self, duration = None):
        '''
        flaps the arms and rolls head from side-to-side

        `duration=None` time limit for motion, in seconds
        '''
        if gestureControl.ARMS_ENABLE:
            self.arms.start(duration)
        # if gestureControl.HEAD_ENABLE:
        #     self.head.startRoll(duration)

    def stop(self):
        '''
        stops arms flapping and head roll
        '''
        if gestureControl.ARMS_ENABLE:
            self.arms.stop()
        if gestureControl.HEAD_ENABLE:
            self.head.stopRoll()
    
    def setHead(self, position_name):
        '''
        move the head to a defined position. eg: 'up', 'mid', 'down'\n
        Positions are defined in the `head_point_dict`. (see __init__())
        '''
        if gestureControl.HEAD_ENABLE:
            self.head.movePoint(position_name)

    def moveHand(self, position = 0.8):
        if gestureControl.ARMS_ENABLE:
            self.arms.hand_standby(position)

if __name__ == "__main__":

    import time
    import rospy
    
    rospy.init_node("test")
    gestureControl.HEAD_ENABLE = True
    obj = gestureControl()
    rospy.loginfo("beginning test run")
    
    obj.setHead("home")
    time.sleep(0.5)
    obj.setHead("left_nod")
    time.sleep(0.5)
    obj.setHead("home")
    time.sleep(0.5)
    obj.setHead("right_nod")
    time.sleep(0.5)
    obj.setHead("home")
    






