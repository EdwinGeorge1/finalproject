#! /usr/bin/env python

import rospy
import time
from jetson_led_control.msg import RGBColor

rospy.init_node("led_tester")
pub = rospy.Publisher("/led_control", RGBColor, queue_size=10)

list_of_colors = [(255,0,0),
                  (0,255,0),
                  (0,0,0),
                  (0,0,255),
                  (0,0,0),
                  (0,0,255),
                  (0,0,0),
                  (0,0,255),
                  (0,0,0),
                  (0,0,255),
                  (0,0,0)]

steps = 40
msg = RGBColor()
pub.publish(msg)
time.sleep(0.5)

while not rospy.is_shutdown():

    steps = 20
    msg = RGBColor()
    pub.publish(msg)
    time.sleep(0.5)

    for i in range(steps):
        msg.B += int((255/steps))
        pub.publish(msg)
        time.sleep(0.05)

    for i in range(steps):
        msg.B -= int((255/steps))
        pub.publish(msg)
        time.sleep(0.05)