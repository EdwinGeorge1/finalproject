#!/usr/bin/env python3


from math import sin, cos, pi

from dynamixel_workbench_msgs.msg import DynamixelStateList
import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3


x = 0.0
y = 0.0
th = 0.0
vx = 0
vy = 0
vth = 0


def VelocityCallback(data):
    global vx
    global vy
    global vth
    left_wheel_vel_rps = (data.dynamixel_state[0].present_velocity * 0.23)/60
    right_wheel_vel_rps = (data.dynamixel_state[1].present_velocity * 0.23)/60
    left_wheel_vel = left_wheel_vel_rps* 2 * pi * 0.075
    right_wheel_vel = right_wheel_vel_rps * 2 * pi * 0.075
    # angular_vel_left = left_wheel_vel / 0.075
    # angular_vel_right = right_wheel_vel / 0.075
    vx = (((left_wheel_vel) + (right_wheel_vel)) / 2)
    vy = 0
    vth = (((right_wheel_vel)- (left_wheel_vel)))/0.25

rospy.init_node('odometry_publisher')

odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)
ticks_sub =rospy.Subscriber("/dynamixel_workbench/dynamixel_state", DynamixelStateList, VelocityCallback)
odom_broadcaster = tf.TransformBroadcaster()

current_time = rospy.Time.now()
last_time = rospy.Time.now()

r = rospy.Rate(60)
while not rospy.is_shutdown():
    current_time = rospy.Time.now()

    # compute odometry in a typical way given the velocities of the robot
    dt = (current_time - last_time).to_sec()
    delta_x = (vx * cos(th) - vy * sin(th)) * dt
    delta_y = (vx * sin(th) + vy * cos(th)) * dt
    delta_th = vth * dt

    x += delta_x
    y += delta_y
    th += delta_th

    # since all odometry is 6DOF we'll need a quaternion created from yaw
    odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)

    # first, we'll publish the transform over tf
    odom_broadcaster.sendTransform(
        (x, y, 0.),
        odom_quat,
        current_time,
        "base_link",
        "odom"
    )

    # next, we'll publish the odometry message over ROS
    odom = Odometry()
    odom.header.stamp = current_time
    odom.header.frame_id = "odom"

    # set the position
    odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))

    # set the velocity
    odom.child_frame_id = "base_link"
    odom.twist.twist = Twist(Vector3(vx, vy, 0), Vector3(0, 0, vth))

    # publish the message
    odom_pub.publish(odom)

    last_time = current_time
    r.sleep()
