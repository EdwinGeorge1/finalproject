import smach
import smach_ros
import rospy
from mbf_msgs.msg import ExePathAction
from mbf_msgs.msg import ExePathResult
from std_msgs.msg import Empty,String
from mbf_msgs.msg import GetPathAction
from mbf_msgs.msg import GetPathResult
from select_pose_or_path import selection
from arduino_serial.msg import RGBColor

if hasattr(smach.CBInterface, '__get__'):
    from smach import cb_interface
else:
    from smach_polyfill import cb_interface


class PlannerStateMachine(smach.StateMachine):
    def __init__(self, concurrency_slot, planner_name, controller_name):
        smach.StateMachine.__init__(
            self,
            outcomes=['preempted', 'succeeded', 'aborted', 'failure'],
            input_keys=['target_pose','path','path_enable'],
            output_keys=['outcome', 'message', 'path'])

        self._concurrency_slot = concurrency_slot
        self._planner_name = planner_name
        self._controller_name = controller_name
        self.pub = rospy.Publisher('way_cmp', String, queue_size=10)
        self.led = rospy.Publisher("/led_control", RGBColor, queue_size=1)

        with self:
            smach.StateMachine.add(
                'SELECTION',
                selection(),
                transitions={
                    'path_sel': planner_name.upper()+'_EXEC',
                    'pose_sel': planner_name.upper()})
            state = smach_ros.SimpleActionState(
                'move_base/get_path',
                GetPathAction,
                goal_cb=self.get_path_goal_cb,
                result_cb=self.get_path_result_cb)
            smach.StateMachine.add(
                planner_name.upper(),
                state,
                transitions={
                    'succeeded': planner_name.upper()+'_EXEC',
                    'failure': 'failure',
                    'preempted': 'preempted'})
            state = smach_ros.SimpleActionState(
                'move_base/exe_path',
                ExePathAction,
                goal_cb=self.exe_path_goal_cb,
                result_cb=self.exe_path_result_cb)
            smach.StateMachine.add(
                planner_name.upper() + '_EXEC',
                state,
                transitions={
                    'succeeded': 'succeeded',
                    'failure': 'failure',
                    'preempted': 'preempted'})

    @cb_interface(input_keys=['target_pose'])
    def get_path_goal_cb(self, userdata, goal):
        goal.use_start_pose = False
        goal.tolerance = 0.2
        goal.target_pose = userdata.target_pose
        goal.planner = self._planner_name
        goal.concurrency_slot = self._concurrency_slot

    @cb_interface(
        output_keys=['message', 'outcome', 'path'],
        outcomes=['succeeded', 'failure'])
    def get_path_result_cb(self, userdata, status, result):
        if result is None:  # something preempted or aborted this
            print('result is None!')
            return 'aborted'

        userdata.message = result.message
        userdata.outcome = result.outcome
        userdata.path = result.path

        if result.outcome == GetPathResult.SUCCESS:
            return 'succeeded'
        elif result.outcome == GetPathResult.CANCELED:
            return 'preempted'
        else:
            print('Planning with %s terminated with non-success status code %s:\n%s' % (self._planner_name, str(result.outcome), result.message))
            return 'failure'

    @cb_interface(input_keys=['path'])
    def exe_path_goal_cb(self, userdata, goal):
        goal.path = userdata.path
        goal.controller = self._controller_name

    @cb_interface(
        output_keys=['outcome', 'message', 'final_pose', 'dist_to_goal'],
        outcomes=['succeeded', 'failure'])
    def exe_path_result_cb(self, userdata, status, result):
        if result:
            userdata.message = result.message
            userdata.outcome = result.outcome
            userdata.dist_to_goal = result.dist_to_goal
            userdata.final_pose = result.final_pose
            if result.outcome == ExePathResult.SUCCESS:
                color = RGBColor()
                color.R = 0
                color.G = 0    
                color.B = 150
                color.T = 0
                self.led.publish(color)
                self.pub.publish("finished")
                return 'succeeded'
            elif result.outcome == ExePathResult.CANCELED:
                return 'preempted'
            else:
                print('Execution of %s terminated with non-success status code %s:\n%s' % (self._planner_name, str(result.outcome), result.message))
                return 'failure'
        else:
            print(status)
            return 'failure'
