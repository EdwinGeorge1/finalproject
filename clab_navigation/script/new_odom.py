#!/usr/bin/env python3


from math import sin, cos, pi

from dynamixel_workbench_msgs.msg import DynamixelStateList
import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

class odom:

    def __init__(self,
                 odom_topic = "odom"):

        self.x = 0.0
        self.y = 0.0
        self.th = 0.0
        self.vx = 0
        self.vy = 0
        self.vth = 0

        self.odom_publisher = rospy.Publisher(odom_topic, Odometry, queue_size=50)

        rospy.Subscriber("/dynamixel_workbench/dynamixel_state", DynamixelStateList, self.velocity_callback)

        self.odom_broadcaster = tf.TransformBroadcaster()

        # self.current_time = rospy.Time.now()
        self.last_time = rospy.Time.now()

        self.rate = rospy.Rate(50)

    def velocity_callback(self, data):

        self.left_wheel_vel_rps = (data.dynamixel_state[0].present_velocity * 0.23)/60
        self.right_wheel_vel_rps = (data.dynamixel_state[1].present_velocity * 0.23)/60

        self.left_wheel_vel = self.left_wheel_vel_rps* 2 * pi * 0.075
        self.right_wheel_vel = self.right_wheel_vel_rps * 2 * pi * 0.075

        self.vx = ((self.left_wheel_vel) + (self.right_wheel_vel)) / 2
        self.vy = 0
        self.vth = (self.right_wheel_vel)- (self.left_wheel_vel)/0.25

    def odom_computation(self):

        while not rospy.is_shutdown():

            self.current_time = rospy.Time.now()

            self.dt = (self.current_time - self.last_time).to_sec()

            self.delta_x = (self.vx * cos(self.th) - self.vy * sin(self.th)) * self.dt

            self.delta_y = (self.vx * sin(self.th) + self.vy * cos(self.th)) * self.dt

            self.delta_th = self.vth * self.dt

            self.odom_quat = tf.transformations.quaternion_from_euler(0, 0, self.th)

            self.odom_broadcaster.sendTransform(
                (self.x, self.y, 0.),
                self.odom_quat,
                self.current_time,
                "base_link",
                "odom"
            )

            self.odom = Odometry()

            self.odom.stamp = self.current_time

            self.odom.header.frame_id = "odom"

            self.odom.pose.pose = Pose(Point(self.x, self.y, 0), Quaternion(*self.odom_quat))

            self.odom.child_frame_id = "base_link"

            self.odom.twist.twist = Twist(Vector3(self.vx, self.vy, 0), Vector3(0, 0, self.vth))

            self.odom_publisher.publish(self.odom)

            self.rate.sleep()
    


if __name__ == "__main__":

    rospy.init_node("odom")

    odom_obj = odom()

    odom_obj.odom_computation()
