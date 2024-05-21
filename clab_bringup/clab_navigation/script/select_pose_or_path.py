import rospy
import smach
import time
from arduino_serial.msg import RGBColor

from geometry_msgs.msg import PoseStamped

from std_msgs.msg import String
from nav_msgs.msg import Path
class selection(smach.State):
    def __init__(self):
        self.led = rospy.Publisher("/led_control", RGBColor, queue_size=1)
        smach.State.__init__(
            self,
            outcomes=['path_sel', 'pose_sel'],
            input_keys=['target_pose','path','path_enable'],
            output_keys=['target_pose','path','path_enable'])

    def execute(self, userdata):
        rospy.loginfo('Executing selection state')
        color = RGBColor()
        color.R = 0
        color.G = 150    
        color.B = 0   
        color.T = 0
        self.led.publish(color)
        if userdata.path_enable :
            rospy.loginfo('selected path')
            return 'path_sel'
        else:
            rospy.loginfo('selected pose')

            return 'pose_sel'
   
