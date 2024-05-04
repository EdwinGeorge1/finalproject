#!/usr/bin/env python3
from GifDisplay import GifDisplay
import rospy
from std_msgs.msg import Empty, String, Int32, Float32
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from arduino_serial.msg import RGBColor
from subprocess import call
import time
import json
from geometry_msgs.msg import PoseStamped
from mutagen.mp3 import MP3
import pygame
# from gestureControl import gestureControl


# paygame initialize for audio play
pygame.init()
pygame.mixer.init()

''' Custom defined modules'''


class flow():
    def __init__(self):
        self.ui_process_started = True
        self.current_process = 0
# publishers
        # this publisher is launch start page
        self.launch_start = rospy.Publisher("/start", String, queue_size=1)
        self.ui_control = rospy.Publisher("/ui_data", String, queue_size=1)
        self.popup_close_pub = rospy.Publisher(
            "/ui_close", String, queue_size=1)
        # self.tray_cnt = rospy.Publisher("/tray_control", String, queue_size=1) "later will be added"
        self.button_control_pub = rospy.Publisher(
            "/button_control", String, queue_size=1)
        self.flag = rospy.Publisher("/flag", String, queue_size=1)
        self.long_speech_gesture = rospy.Publisher(
            '/long_speech_gesture', Int32, queue_size=10)

# publisher for navigation
        self.goal_publish = rospy.Publisher(
            "move_base_simple/goal", PoseStamped)
        self.cancel_goal = rospy.Publisher("move_base/cancel", String)

# Led Strip
        self.led = rospy.Publisher("/led_control", RGBColor, queue_size=1)
        # self.led_color = rospy.Publisher("/mood_light", String, queue_size=10)

        # subscriber ui and ros communication
        rospy.Subscriber('/way_cmp', String, self.nav_cb, queue_size=1)
        rospy.Subscriber('/button', String, self.button_cb, queue_size=1)
        rospy.Subscriber('/start_ui', String, self.ui_button_cb, queue_size=1)
        rospy.Subscriber('/wakeup_lidar', Bool,
                         self.blank_screen_cb, queue_size=1)
        rospy.Subscriber('/battery_voltage', Float32, self.battery_callback)

        self.robot_current_position = 0
        self.robot_previous_position = 0
        self.nav_result = ""

        # joystick 
        self.navigating = False
        self.shutdown_cnt = 0
        self.restart_cnt = 0
        self.cmd_repub = rospy.Publisher(
            "/diffbot_controller/cmd_vel", Twist, queue_size=1)  # self.stop_audio()
        rospy.Subscriber("/joy", Joy, self.joy_cb, queue_size=1)

        ''' Adding GIF file for navigating with happy face '''
        self.happy_gif = GifDisplay('~/clab_ws/src/clab/gif_files/happy.mp4')

        
        ''' NAVIGATION'''
# Navigation goals should be added here

        self.goals = {"home": {"x": 0.6916, "y": 2.1305, "z": 0.3809, "w": 0.9245},

                      "brijesh": {"x": 1.4209, "y": -2.416, "z": -0.6081, "w": 0.7938},

                      "prasad": {"x": 0.0227, "y": 4.3203, "z": -0.9265, "w": 0.3760},

                      "sujith": {"x": 1.2420, "y": 3.0878, "z": -0.3649, "w": 0.9310},

                      "chandan": {"x": 1.8873, "y": 2.2822, "z": 0.9369, "w": 0.3493},

                      "spirestone": {"x": 1.3004, "y": -2.1124, "z": 0.2971, "w": 0.9548},

                      "wemoswitch": {"x": 2.0641, "y": -0.9994, "z": 0.4361, "w": 0.8998},

                      "dropstop": {"x": 3.1365, "y": 0.8126, "z": -0.0354, "w": 0.9993}

                      }


#   Navigation  satus feedback 

    def nav_cb(self, data):
        try:

            self.nav_result = data.data
        except Exception as e:
            print("nav_cb:", e)


# """ LEAD AND BATTERY """

# ''' Call back function wake up screen when a user infront of robot'''

    def blank_screen_cb(self, data):

        if data.data == 1:
            self.close_image()


    ''' This function is a publisher for lead color '''
    def led_color(self, r=0, g=0, b=0, t=0):
        color = RGBColor()
        color.R = r
        color.G = g
        color.B = b
        color.T = t
        try:

            self.led.publish(color)
        except Exception as e:
            print("led_color: ", e)

    def movebase_publish(self, goal_x, goal_y, goal_z, goal_w):
        global goal_publish

        goalId = 0
        goalMsg = PoseStamped()
        goalMsg.header.frame_id = "map"
        goalMsg.pose.orientation.z = goal_z
        goalMsg.pose.orientation.w = goal_w
        # Publish the first goal

        goalMsg.header.stamp = rospy.Time.now()
        goalMsg.pose.position.x = goal_x
        goalMsg.pose.position.y = goal_y
        self.goal_publish.publish(goalMsg)
        # self.led_color(g=255)
        print("goal published", goal_x, goal_y)

    def navigate_with_position(self, name):
        self.nav_result = ""
        self.movebase_publish(self.goals[name]["x"], self.goals[name]["y"], self.goals[name]["z"],
                              self.goals[name]["w"])
        while not rospy.is_shutdown():
            time.sleep(0.5)
            if self.nav_result != "":
                self.nav_result = ""
                self.navigating = False
                return
        self.navigating = False
        self.cancel_goal.publish("")



# Joystick call back function

    def joy_cb(self, data):

        if data.buttons[0] == 1:
            print("button X")
            self.exec_gesture("up")

        if data.buttons[3] == 1:
            print("button Y")
            self.exec_gesture("down")

        if data.buttons[8] == 1:
            print("button Back")
            self.shutdown_pressed = True
            shut_thread = threading.Thread(target=self.holding_shutdown_check)
            shut_thread.start()
        else:
            self.shutdown_pressed = False

        if data.buttons[9] == 1:
            print("button Start")
            self.restart_pressed = True
            restart_thread = threading.Thread(
                target=self.holding_restart_check)
            restart_thread.start()
        else:
            self.restart_pressed = False

        if data.buttons[5] == 1:
            print("button RB")
            self.start_audio_gesture("wishes_new")
#            self.tray_cnt.publish("open")

        if data.buttons[1] == 1:
            print("button A")
            self.start_audio("Welcome_CM")

        if data.buttons[2] == 1:
            print("button B")
            self.exec_gesture("move_gesture")

        if data.buttons[4] == 1:
            print("button LB")
            self.exec_gesture("wishes_new")

        if data.buttons[7] == 1:
            print("button RT")
            self.nav_ended = "done"

        if data.buttons[6] == 1:
            print("button LT")
            loli = threading.Thread(
                target=self.exec_gesture, args=('move_gesture',))
            loli.start()
            time.sleep(1)
            self.start_audio("Welcome_CM")
#            self.exec_gesture("down_salute")




# Button callback function and assigned

    def button_cb(self, data):
        try:

            dict1 = json.loads(data.data)
            self.button_pressed = dict1["button"]
            print(dict1)
        except Exception as e:
            print("button_cb :", e)
       
        
# this function is using for testing Purpose GIF open_image  and close_image
    def open_image(self, name):
        call('sh /~/main_ws/src/clab/saya_bringup/script/show_image.sh ' + name, shell=True)

    def close_image(self):
        call('sh /home/jetson/clab_ws/src/clab/saya_bringup/script/close_image.sh', shell=True)

    

# This function for audio playing subprocess.call()

    def exec_audio(self, name):

        self.gesture_control.start()
        call('mpg123 /home/jetson/clab_ws/src/clab/audios/' +
             name + '.mp3', shell=True)
        self.gesture_control.stop()
        # return

    
 # this function for audio playing
    def start_audio(self, audio_name):

        # duration = self.check_audio_timing(audio_name)
        pygame.mixer.music.load(
            '/home/jetson/clab_ws/src/clab/audios/' + audio_name + '.mp3')
        print(audio_name)
        pygame.mixer.music.play()
        # self.gesture_control.start()
        # print(duration)
        # time.sleep(duration)

        # self.gesture_control.stop()
        # self.hand_gest(duration)
        print("audio playing")
        return

    def stop_audio(self):
        ''' Checking any audio playing then stop '''
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            print("audio stoped")


# this function for auto start page came on robot in home position
    def call_startpage(self):
        ''' This fun for to open start button page means start.php'''
        msg = String()
        msg.data = "hello"
        try:

            self.launch_start.publish(msg)
        except Exception as e:
            print(e)
        print("call_startpage fun ")
        return

# this function for kill audio playing using  while a playing audio using subprocess

    def close_music(self):
        call('pkill mpg123', shell=True)

 # This function return audio duration type : int
    def check_audio_timing(self, name):

        fname = "/home/jetson/clab_ws/src/clab/audios/" + name + ".mp3"
        duration = 0
        audio = MP3(fname)
        duration = int(audio.info.length)
        audio.delete()
        return duration

    
        # this function for call robot to move home position

    def return_to_home(self):
        while not rospy.is_shutdown():
            time.sleep(20)
            # self.navigate_with_position('home')
            print('goal position reached')
            self.current_process = 2
            return

# 0  this for Home page 
    def home_page(self):

        self.button_pressed = ''

        while not rospy.is_shutdown():
            if self.button_pressed == "start-button":
                # self.exec_audio_block_gesture('hello')
                # self.start_audio("hello")
                # self.audio_hand_gest("hello")
                self.current_process = 1
                # time.sleep(3)
                # msg = String()
                # msg.data = "hello"
                # self.launch_start.publish(msg)
                # print("after launch")
                return
# 1
    # back page on home page start.php

    def back_skip(self):

        self.button_pressed = ''

        while not rospy.is_shutdown():
            if self.button_pressed == "video-back-button":
                self.stop_audio()
                # self.close_music()

                print("bk pressed")
                self.current_process = 0
                return

            if self.button_pressed == "video-skip-button":
                self.stop_audio()
                # self.close_music()

                print("skip_pressed")
                self.start_audio('please_choose')
                self.current_process = 2
                return
# 2
        # this function for start-01.php
    def options_showing(self):
        print("option showing")

        self.button_pressed = ''
        while not rospy.is_shutdown():

            if self.button_pressed == "clab-tour-button":
                self.stop_audio()
                print("clab")
                self.start_audio('creative_lab_tour')
                self.current_process = 3
                return

            if self.button_pressed == "clab-team-member":
                print("team members")
                self.stop_audio()
                self.start_audio('willguideyou')
                print("after start_audio")
                self.current_process = 4
                return

            if self.button_pressed == "fab_lab-support-button":
                self.stop_audio()
                self.start_audio('willguideyou')
                self.current_process = 5
                return

            if self.button_pressed == "gimba-button":
                self.current_process = 6
                return


# 3    This for clab_tour.php

    def creative_lab_tour(self):
        self.button_pressed = ""

        while not rospy.is_shutdown():

            if self.button_pressed == "clab-tour-skip-button":
                self.creative_lab()
                return

            if self.button_pressed == "clab-tour-back-button":
                self.stop_audio()
                self.current_process = 2
                return
# this for product.php
    def creative_lab(self):

        while self.button_pressed == "clab-tour-skip-button":

            self.stop_audio()
            self.happy_gif.open()
            # self.navigate_with_position('spirestone')
            self.happy_gif.close()
            self.exec_audio('spirestone')
            # self.play_music("spirestone.mp3")
            if self.button_pressed != "clab-tour-skip-button":
                self.close_music()
                self.current_process = 2
                break
            time.sleep(2)
            self.flag.publish()

            # self.happy_gif.open()
            # time.sleep(4)
            # # self.navigate_with_position('wemoswitch')
            # self.happy_gif.close()
            # self.play_music("wemoswitch.mp3")
            # # self.exec_audio('wemoswitch')
            # if self.button_pressed != "clab-tour-skip-button":
            #     self.close_music()
            #     self.current_process = 2
            #     break
            # time.sleep(2)
            # self.flag.publish()

            # self.happy_gif.open()
            # time.sleep(4)
            # self.navigate_with_position('dropstop')
            # self.happy_gif.close()
            # self.start_audio('dropstop')
            # self.happy_gif.open()
            # time.sleep(4)
            # self.navigate_with_position('home') # this statement for testing purpose
            # if self.button_pressed != "clab-tour-skip-button":
            #     self.current_process = 2
            #     return
            # time.sleep(2)
            # self.flag.publish()

            # self.navigate_with_position()
            # self.start_audio('grophesense')
            # if self.button_pressed != "clab-tour-skip-button":
            #     self.current_process = 2
            #     break
            # time.sleep(2)
            # self.flag.publish()

            # self.navigate_with_position()
            # self.start_audio('miniprojector')
            # if self.button_pressed != "clab-tour-skip-button":
            #     self.current_process = 2
            #     break
            # time.sleep(2)
            # self.flag.publish()

            # self.navigate_with_position()
            # self.start_audio('rollr')
            # if self.button_pressed != "clab-tour-skip-button":
            #     self.current_process = 2
            #     break
            # time.sleep(2)
            # self.flag.publish()

            # self.navigate_with_position()
            # self.start_audio('keyboard')
            # if self.button_pressed != "clab-tour-skip-button":
            #     self.current_process = 2
            #     break
            # time.sleep(2)
            # self.flag.publish()

            # self.navigate_with_position()
            # self.start_audio('solar')
            # if self.button_pressed != "clab-tour-skip-button":
            #     self.current_process = 2
            #     break
            # time.sleep(2)
            # self.flag.publish()

            # self.navigate_with_position()
            # self.start_audio('blue_globe')
            # if self.button_pressed != "clab-tour-skip-button":
            #     self.current_process = 2
            #     break
            # time.sleep(2)
            # self.flag.publish()

            # self.navigate_with_position()
            # self.start_audio('ztylus')
            # if self.button_pressed != "clab-tour-skip-button":
            #     self.current_process = 2
            #     break
            # time.sleep(2)
            # self.flag.publish()

            if self.button_pressed != "clab-tour-skip-button":
                self.current_process = 2
                break

# 4 for team_members.php
    def team_member(self):
        print("team member fun")
        self.button_pressed = ''

        while not rospy.is_shutdown():

            if self.button_pressed == "brijesh-button":
                print("gif open")
                self.happy_gif.open()
                # self.navigate_with_position('brijesh')
                self.happy_gif.close()
                print('I am brijesh')
                self.start_audio('reached_destination')
                # self.return_to_home()
                return

            if self.button_pressed == "prasad-button":
                self.happy_gif.open()
                time.sleep(4)
                # self.navigate_with_position('prasad')
                self.happy_gif.close()
                print("I am prasad")
                self.start_audio('reached_destination')
                return

            if self.button_pressed == "sujith-button":
                self.happy_gif.open()
                time.sleep(2)
                # self.navigate_with_position('sujith')
                self.happy_gif.close()
                print("I am sujith")
                self.start_audio('reached_destination')
                return

            if self.button_pressed == "chandan-button":
                self.happy_gif.open()
                time.sleep(2)
                # self.navigate_with_position('chandran')
                self.happy_gif.close()
                print("I am chandan")
                self.start_audio('reached_destination')
                return

            if self.button_pressed == "deepak-button":
                # self.navigate_with_position('table1')
                print("I am deepak")
                # self.start_audio('reached_destination')
                return

            if self.button_pressed == "hariprakash-button":
                # self.navigate_with_position('table2')
                print("I am hariprakash")
                self.start_audio('reached_destination')
                return

            if self.button_pressed == "back-button":
                # self.navigate_with_position('home')
                # self.call_startpage()
                self.current_process = 2
                return

# 5 for fab_lab_support.php
    def fab_lab_support(self):

        self.button_pressed == ''

        while not rospy.is_shutdown():

            if self.button_pressed == "electronics-support-button":
                self.current_process = 7
                return

            if self.button_pressed == "mech-support-button":
                self.current_process = 8
                return

            if self.button_pressed == "fabrication-support-button":
                self.current_process = 9
                return

            if self.button_pressed == "fab-support-back-button":
                self.current_process = 2
                return

# 6 for gemba.php
    def gemba(self):

        self.button_pressed = ""

        while not rospy.is_shutdown():

            if self.button_pressed == "gamba-back-button":
                self.current_process = 2
                return

# 7 for electrical-support.php
    def eletrical_and_electronics_support(self):

        self.button_pressed = ''

        while not rospy.is_shutdown():

            if self.button_pressed == "chandan-button":
                print('I am chandan')
                return

            if self.button_pressed == "ele-back-button":
                self.current_process = 5
                return
# 8 for mechanical-support.php

    def mechanical_support(self):

        self.button_pressed = ''

        while not rospy.is_shutdown():

            if self.button_pressed == "sujith-button":
                print('I am sujith')
                return

            if self.button_pressed == "deepak-button":
                print('I am deepak')
                return

            if self.button_pressed == "mech-support-back-button":
                self.current_process = 5
                return
# 9 for fabrication-support.php

    def fabrication_support(self):
        self.button_pressed = ''

        while not rospy.is_shutdown():

            if self.button_pressed == "sujith-button":
                print('I am sujith')
                return

            if self.button_pressed == "fabricatin-back-button":
                self.current_process = 5
                return

    def main_process(self):
        self.current_process = 0

        while not rospy.is_shutdown():
            time.sleep(1)

            print(self.current_process)

            if self.current_process == 0:
                print(self.current_process)
                self.home_page()

            elif self.current_process == 1:
                print(self.current_process)
                self.back_skip()

            elif self.current_process == 2:
                print(self.current_process)
                self.options_showing()

            elif self.current_process == 3:
                print(self.current_process)
                self.creative_lab_tour()

            elif self.current_process == 4:
                print(self.current_process)
                self.team_member()

            elif self.current_process == 5:
                print(self.current_process)
                self.fab_lab_support()

            elif self.current_process == 6:
                print(self.current_process)
                self.gemba()

            elif self.current_process == 7:
                print(self.current_process)
                self.eletrical_and_electronics_support()

            elif self.current_process == 8:
                print(self.current_process)
                self.mechanical_support()

            elif self.current_process == 9:
                print(self.current_process)
                self.fabrication_support()


if __name__ == '__main__':
    rospy.init_node("main_flow", anonymous=True)
    test = flow()
    test.main_process()
