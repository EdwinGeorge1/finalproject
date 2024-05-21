#!/usr/bin/env python3
import rospy
import smach
import smach_ros
import os
from mbf_msgs.msg import RecoveryAction
from mbf_msgs.msg import RecoveryResult
from arduino_serial.msg import RGBColor
#from std_msgs.msg import Empty
from std_srvs.srv import Empty
from std_msgs.msg import String
from wait_for_goal import WaitForGoal
from geometry_msgs.msg import PoseStamped, Twist

from smach_polyfill import cb_interface
from plan_exec_sm import PlanExecStateMachine
from nav_msgs.msg import Path
from actionlib_msgs.msg import GoalID

class MBFStateMachine(smach.StateMachine):
    _recovery_behaviors = None

    @classmethod
    def set_recovery_behaviors(cls, recovery_behaviors):
        cls._recovery_behaviors = recovery_behaviors

    def set_zero_velocity(self):
        twist_msg = Twist()
        self.pub_zero_velocity.publish(twist_msg)

    def code_red(self):
        color = RGBColor()
        color.R = 150
        color.G = 0    
        color.B = 0   
        color.T = 0
        self.led.publish(color)    

    def __init__(self):
        self.cancel_goal = False
        if self._recovery_behaviors is None:
            raise ValueError("you have to set up planners first by calling MBFStateMachine.set_recovery_behaviors([...]).")

        smach.StateMachine.__init__(self, outcomes=['preempted', 'aborted'])
        self.userdata.recovery_behavior_index = 0  # start with first recovery behavior
        self.pub_zero_velocity = rospy.Publisher('/dynamixel_workbench/cmd_vel', Twist, queue_size=10)
        self.led = rospy.Publisher("/led_control", RGBColor, queue_size=1)
        self.clear_map = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
        self.stop_local_planner = rospy.Publisher('/move_base/exe_path/cancel', GoalID, queue_size=1)
        self.stop_global_planner = rospy.Publisher('/move_base/get_path/cancel', GoalID, queue_size=1)
        self.set_zero_velocity()
        with self:
            smach.StateMachine.add(
                'WAIT_FOR_GOAL',
                WaitForGoal(),
                transitions={
                    'succeeded': 'PLAN_EXEC',
                    'preempted': 'preempted'})

            smach.StateMachine.add(
                'RECOVERY',
                smach_ros.SimpleActionState(
                    'move_base/recovery',
                    RecoveryAction,
                    goal_cb=self.recovery_goal_cb,
                    preempt_timeout = rospy.Duration(0.1),
                    result_cb=self.recovery_result_cb),
                transitions={
                    'succeeded': 'PLAN_EXEC',
                    'preempted': 'preempted',
                    'failure': 'WAIT_FOR_GOAL'})

            plan_exec_sm = PlanExecStateMachine()
            smach.StateMachine.add(
                'PLAN_EXEC',
                plan_exec_sm,
                transitions={
                    'failure': 'RECOVERY',
                    'succeeded': 'WAIT_FOR_GOAL'})

    @cb_interface(input_keys=['recovery_behavior_index'], output_keys=['recovery_behavior_index'])
    def recovery_goal_cb(self, userdata, goal):
        # TODO implement a more clever way to call the right behavior. Currently cycles through all behaviors
        behavior = self._recovery_behaviors[userdata.recovery_behavior_index]
        print ('RECOVERY BEHAVIOR:', behavior)
        goal.behavior = behavior
        userdata.recovery_behavior_index += 1
        if userdata.recovery_behavior_index >= len(self._recovery_behaviors):
            userdata.recovery_behavior_index = 0

    @cb_interface(output_keys=['outcome', 'message','path_enable'], outcomes=['succeeded', 'preempted', 'failure'])
    def recovery_result_cb(self, userdata, status, result):
        if result.outcome == RecoveryResult.SUCCESS:
            self.code_red()
            os.system(" mpg123 /home/jetson/clab_ws/src/clab/audios/audio_obs_avoid.mp3")
            rospy.logerr("sleeping")
            resp = self.clear_map()
            rospy.sleep(4)
            if self.cancel_goal == True:
                return 'preempted'
            return 'succeeded'
        elif result.outcome == RecoveryResult.CANCELED:
            self.set_zero_velocity()
            rospy.logerr("changing plan")
            userdata.path_enable = False # if recovery fails during path following mode, it changes to target_pose mode
            return 'preempted'
        else:
            rospy.logerr("changing plan")
            userdata.path_enable = False # if recovery fails during path following mode, it changes to target_pose mode
            self.set_zero_velocity()
            return 'failure'
    def stop_local_plan(self):
        goal = GoalID()
        self.stop_local_planner.publish(goal)
        self.set_zero_velocity()

    def stop_global_plan(self):
        goal = GoalID()
        self.stop_global_planner.publish(goal)

#    def request_preempt(self):
#        """Overload the preempt request method just to spew an error."""
#        smach.StateMachine.request_preempt(self)
#        rospy.logwarn("Preempted!")


SM = None
SM_target_pose = None
cancelling_goal = True
def cancel_callback(data):
    global cancelling_goal, SM_target_pose
    if SM is not None and SM.get_active_states()[0] != 'WAIT_FOR_GOAL':
        # SM.stop_global_plan()
        cancelling_goal = True
        SM_target_pose = None
        SM.cancel_goal = True
        SM.stop_local_plan()
        print("------------------------------------------")
        SM.request_preempt()


def goal_callback(target_pose):
    #clear the costmap before proceeding
    global SM_target_pose, cancelling_goal

    if cancelling_goal:
        SM_target_pose = target_pose
        return
    elif SM is not None and SM.get_active_states()[0] != 'WAIT_FOR_GOAL':

        SM.cancel_goal = True
        SM.request_preempt()

        SM_target_pose = target_pose


if __name__ == '__main__':
    rospy.init_node('mbf_state_machine')

    subscriber = rospy.Subscriber('/move_base_simple/goal', PoseStamped, goal_callback)
    cancel_sub = rospy.Subscriber('/move_base/cancel', String, cancel_callback)

    while not rospy.is_shutdown():

        planners = [entry['name'] for entry in rospy.get_param('/move_base/planners')]
        if len(planners) == 0:
            raise ValueError('You have to specify at least one planner')
        PlanExecStateMachine.set_planners(planners)




        recovery_behaviors = [entry['name'] for entry in rospy.get_param('/move_base/recovery_behaviors')]
        MBFStateMachine.set_recovery_behaviors(recovery_behaviors)

        SM = MBFStateMachine()

        sis = smach_ros.IntrospectionServer('mbf_state_machine_server', SM, '/MBF_SM')
        print("*****************************")
        if SM_target_pose is not None:
            SM.userdata._data = {}
            SM.userdata.recovery_behavior_index = 0

            target_userdata = smach.UserData()
            target_userdata.target_pose = SM_target_pose
            target_userdata.path = Path()
            target_userdata.path_enable = False
            SM.set_initial_state(['PLAN_EXEC'], userdata=target_userdata)
            SM_target_pose = None

        cancelling_goal = False
        outcome = SM.execute()
        sis.stop()
