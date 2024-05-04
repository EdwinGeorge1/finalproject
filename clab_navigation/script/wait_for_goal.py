import time
import rospy
import smach
import csv
from geometry_msgs.msg import PoseStamped
from std_srvs.srv import Empty
from std_msgs.msg import String
from nav_msgs.msg import Path
class WaitForGoal(smach.State):
    def __init__(self):
        smach.State.__init__(
            self,
            outcomes=['succeeded', 'preempted'],
            output_keys=['target_pose','path','path_enable'])
        self._global_target_pose = PoseStamped()
        self._subscriber = None
        self._subscriber1 = None
        self._flag_goal_received = False
        self.clear_map_ = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
        self._path = Path()
        self._path_enable = False

    def execute(self, userdata):
        self._flag_goal_received = False
        self._subscriber = rospy.Subscriber('/move_base_simple/goal', PoseStamped, self.goal_callback) # looking for the target pose
        self._subscriber1 = rospy.Subscriber('/global_path_location', String, self.goal_callback1) # looking for the path
        rate = 0.3
        while not self._flag_goal_received and not rospy.is_shutdown():
            time.sleep(rate)

        resp1 = self.clear_map_()
        time.sleep(1)
        userdata.target_pose = self._global_target_pose
        userdata.path = self._path
        userdata.path_enable = self._path_enable
        print("Target Pose:", self._global_target_pose.pose.position.x, self._global_target_pose.pose.position.y,\
              self._global_target_pose.pose.position.z)
        if rospy.is_shutdown():
          return 'preempted'

        return 'succeeded'
    # callback will be called if the target pose is given
    def goal_callback(self, msg):
        print("Received goal:")
        self._global_target_pose = msg
        self._subscriber.unregister()
        self._subscriber1.unregister()
        self._flag_goal_received = True
        self._path_enable = False
    # callback will be called if the path  is given
    def goal_callback1(self, msg):
        glob_path = Path()
        no_of_points = 0
    
        with open(msg.data) as csvfile:
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
                glob_path.poses.append(pose)
                self._global_target_pose = pose
                no_of_points += 1
        print("{} points are readed".format(no_of_points))
        self._path = glob_path
        self._subscriber1.unregister()
        self._subscriber.unregister()
        self._flag_goal_received = True
        self._path_enable = True

