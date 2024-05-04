#!/usr/bin/env python

# ROS IMPORTS
import rospy
from std_msgs.msg import String, Float32
from std_msgs.msg import Bool
from sensor_msgs.msg import Joy
from arduino_serial.msg import RGBColor
from geometry_msgs.msg import PoseStamped

# PYTHON IMPORTS
from subprocess import call
import time
import json
from mutagen.mp3 import MP3
import pygame

# OUR OWN MODULES IMPORTS
from gestureControl import gestureControl
from GifDisplay import GifDisplay

# ENABLE THIS SO THAT ARMS CAN WORK
# <<<<<<< HEAD
# gestureControl.ARMS_ENABLE = True
# gestureControl.HEAD_ENABLE = False  
# =======
# gestureControl.ARMS_ENABLE = False
# gestureControl.HEAD_ENABLE = False
# # >>>>>>> ff49398698ee27feca9a4f82d3d2cda8264ebd77

# PYGAME INITIALIZING FOR PLAYING AUDIO
pygame.init()
pygame.mixer.init()


# INITIALIZING CLASS

class flow():
    def __init__(self):

        # ROS PUBLISHERS

        # THIS PUB BRINGS BACK UI TO START PAGE
        self.launch_start = rospy.Publisher("/start", String, queue_size=1)

        # THIS PUB CHANGES THE PRODUCT IN PRODUCT PAGE
        self.flag = rospy.Publisher("/flag", String, queue_size=1)

        # PUBLISHERS FOR NAVIGATION
        self.goal_publish = rospy.Publisher("move_base_simple/goal", PoseStamped)
        self.cancel_goal = rospy.Publisher("move_base/cancel", String)

        # PUBLISHER FOR LED STRIP
        self.led = rospy.Publisher("/led_control", RGBColor, queue_size=1)

        # ROS SUBSCRIBERS

        # NAV RESULT SUB
        rospy.Subscriber('/way_cmp', String, self.nav_cb, queue_size=1)

        # BUTTON FEEDBACK SUB
        rospy.Subscriber('/button', String, self.button_cb, queue_size=1)

        # LIDAR FEEDBACK SUB
        rospy.Subscriber('/wakeup_lidar', Bool, self.blank_screen_cb, queue_size=1)
        rospy.Subscriber('/battery_voltage', Float32, self.battery_callback)
        rospy.Subscriber("/joy", Joy, self.joy_cb, queue_size=1)

        # ATTRIBUTES NEEDED FOR METHODS
        self.current_process = 0
        self.nav_result = ""
        self.navigating = False

        # CREATING OBJECT FOR GIF DISPLAY CLASS
        self.happy_gif = GifDisplay('/home/jetson/clab_ws/src/clab/gif_files/happy.mp4')

# <<<<<<< HEAD
#CREATING OBJECT FOR GESTURE CONTROL CLASS 
        self.gesture_control = gestureControl()
# =======
        # CREATING OBJECT FOR GESTURE CONTROL CLASS
#         self.gesture_control = gestureControl("")
# >>>>>>> ff49398698ee27feca9a4f82d3d2cda8264ebd77

        # ALL THE GOAL POSITIONS SHOULD BE MENTIONED HERE BEFORE CALLING THEM

        self.goals = {"home": {"x": 0.6916, "y": 2.1305, "z": 0.3809, "w": 0.9245},

                      "brijesh": {"x": 1.4209, "y": -2.416, "z": -0.6081, "w": 0.7938},

                      "prasad": {"x": 0.0227, "y": 4.3203, "z": -0.9265, "w": 0.3760},

                      "sujith": {"x": 1.2420, "y": 3.0878, "z": -0.3649, "w": 0.9310},

                      "chandan": {"x": 1.8873, "y": 2.2822, "z": 0.9369, "w": 0.3493},

                      "spirestone": {"x": 1.3004, "y": -2.1124, "z": 0.2971, "w": 0.9548},

                      "wemoswitch": {"x": 2.0641, "y": -0.9994, "z": 0.4361, "w": 0.8998},

                      "dropstop": {"x": 3.1365, "y": 0.8126, "z": -0.0354, "w": 0.9993}

                      }

    # THIS CALLBACK METHOD WAKES THE SCREEN ON
    def blank_screen_cb(self, data):

        if data.data == 1:
            self.close_image()

    # THIS METHODS WHEN CALLED WITH RGBT VALUES PUBLISHES COLOR VALUES TO LED
    def led_color(self, r=0, g=0, b=0, t=0):
        color = RGBColor()
        color.R = r
        color.G = g
        color.B = b
        color.T = t
        self.led.publish(color)

    # THIS CALLBACK METHOD PUTS ON A SAD ANIMATION WHEN BATTERY VOLT IS LOW
    def battery_callback(self, data):
        self.voltage = data.data

        if self.voltage < 10:
            print("low_battery")
            self.show_video('animated.gif')

    # THIS CALLBACK METHOD IS FOR JOYSTICK BASED CONTROL
    def joy_cb(self, data):

        if data.buttons[0] == 1:
            print("button X")
            pass

        if data.buttons[3] == 1:
            print("button Y")
            pass

        if data.buttons[8] == 1:
            print("button Back")
            pass

        if data.buttons[9] == 1:
            print("button Start")
            pass

        if data.buttons[5] == 1:
            print("button RB")
            pass

        if data.buttons[1] == 1:
            print("button A")
            pass

        if data.buttons[2] == 1:
            print("button B")
            pass

        if data.buttons[4] == 1:
            print("button LB")
            pass

        if data.buttons[7] == 1:
            print("button RT")
            pass

        if data.buttons[6] == 1:
            print("button LT")
            pass

    # THIS CALLBACK METHOD CHECKS FOR NAV RESULT
    def nav_cb(self, data):
        self.nav_result = data.data

    # THIS CALLBACK METHOD GIVES THE BUTTON PRESSED FEEDBACK FROM UI
    def button_cb(self, data):
        dict1 = json.loads(data.data)
        print("button data")
        print(dict1)
        self.button_pressed = dict1["button"]

    # THIS METHOD IS OPEN IMAGE FILE WHEN NEEDED
    def open_image(self, name):
        call('sh /home/jetson/clab_ws/src/clab/saya_bringup/script/show_image.sh ' + name, shell=True)

    # THIS METHOD IS CLOSE IMAGE FILE WHEN NEEDED
    def close_image(self):
        call('sh /home/jetson/clab_ws/src/clab/saya_bringup/script/close_image.sh', shell=True)

    # THIS METHOD IS TO START AUDIO ALONG WITH HAND AND HEAD GESTRUE
    def start_audio(self, audio_name):

        duration = self.check_audio_timing(audio_name)
        pygame.mixer.music.load('/home/jetson/clab_ws/src/clab/audios/' + audio_name + '.mp3')
        print(audio_name)
        pygame.mixer.music.play()
        self.gesture_control.start(duration)
        # self.gesture_control.stop()
        # self.hand_gest(duration)
        print("audio playing")
        return

    # THIS METHOD IS TO STOP THE PLAYING AUDIO AND GESTURES
    def stop_audio(self):
        ''' Checking any audio playing then stop '''
        if pygame.mixer.music.get_busy():
            self.gesture_control.stop()
            pygame.mixer.music.stop()
            print("audio stoped")

    # THIS METHOD WHEN CALLED MOVES THE UI PAGE TO START PAGE
    def call_startpage(self):
        ''' This fun for to open start button page means start.php'''
        msg = String()
        msg.data = "hello"
        self.launch_start.publish(msg)
        print("call_startpage fun ")
        return

    # THIS METHOD IS OPEN GIF FILE WHEN NEEDED

    def show_video(self, name):
        call('sh /home/jetson/clab_ws/src/clab/saya_bringup/script/show_gif.sh ' + name, shell=True)

    # THIS METHOD IS CLOSE GIF FILE WHEN NEEDED

    def close_video(self):
        call('sh /home/jetson/clab_ws/src/clab/saya_bringup/script/close_gif.sh', shell=True)

    # BELOW TWO METHOD SERVES PRODUCT PAGE

    # THIS METHOD CHECKS FOR BUTTON FEEDBACK, AND STOPS AUDIO AND HELPS BREAKING LOOP
    def product_page_audio_stop_cb(self):
        while pygame.mixer.music.get_busy():
            if self.button_pressed == 'product-home-button':
                self.stop_audio()
                return self.button_pressed

        return self.button_pressed

    # THIS METHOD HELPS PRODUCT PAGE TO MOVE TO NEXT PRODUCT WITH CERTAIN TIME DELAY
    def product_page_change(self):
        time.sleep(2)
        self.flag.publish()
        return

    # THIS METHOD RETURNS DURATION OF THE AUDIO
    def check_audio_timing(self, name):

        fname = "/home/jetson/clab_ws/src/clab/audios/" + name + ".mp3"
        duration = 0
        audio = MP3(fname)
        duration = int(audio.info.length)
        audio.delete()
        return duration

    # THIS METHOD WRITES THE GOAL POSITION FOR THE CONTROLLER
    def movebase_publish(self, goal_x, goal_y, goal_z, goal_w):
        global goal_publish

        goalId = 0
        goalMsg = PoseStamped()
        goalMsg.header.frame_id = "map"
        goalMsg.pose.orientation.z = goal_z
        goalMsg.pose.orientation.w = goal_w

        goalMsg.header.stamp = rospy.Time.now()
        goalMsg.pose.position.x = goal_x
        goalMsg.pose.position.y = goal_y
        self.goal_publish.publish(goalMsg)
        # self.led_color(g=255)
        print("goal published", goal_x, goal_y)

    # THIS METHOD IS CALLED TO GIVE THE NAME DESTINATION TO BE REACHED
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

    # THIS METHOD RETURNS ROBOT TO THE HOME POSITON AFTER CERTAIN TIME
    def return_to_home(self):
        while not rospy.is_shutdown():
            time.sleep(20)
            # self.navigate_with_position('home')
            print('goal position reached')
            self.current_process = 2
            return

    # BELOW METHODS ARE THE MAIN PROCESS

    # 0 START PAGE
    def home_page(self):

        self.button_pressed = ''

        while not rospy.is_shutdown():
            if self.button_pressed == "start-button":
                self.start_audio("hello")
                self.current_process = 1
                return

    # 1 BACK_SKIP PAGE

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

    # 2 OPTIONS SHOWING PAGE

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

    # 3 BACK SKIP PAGE 2

    def back_skip_2(self):
        self.button_pressed = ""

        while not rospy.is_shutdown():

            if self.button_pressed == "clab-tour-skip-button":
                self.current_process = 10
                return

            if self.button_pressed == "clab-tour-back-button":
                self.stop_audio()
                self.current_process = 2
                return

    # 10 CREATIVE LAB TOUR STARTS HERE
    def creative_lab_tour(self):

        while not rospy.is_shutdown():

            if self.button_pressed == "clab-tour-skip-button":
                self.stop_audio()
                self.happy_gif.open()
                self.navigate_with_position('spirestone')
                self.happy_gif.close()
                self.start_audio('spirestone')
                self.product_page_audio_stop_cb()
                if self.product_page_audio_stop_cb() == "product-home-button":
                    self.current_process = 2
                    break
                self.product_page_change()

                self.happy_gif.open()
                self.navigate_with_position('wemoswitch')
                self.happy_gif.close()
                self.start_audio('wemoswitch')
                self.product_page_audio_stop_cb()
                if self.product_page_audio_stop_cb() == "product-home-button":
                    self.current_process = 2
                    break
                self.product_page_change()

                self.happy_gif.open()
                self.navigate_with_position('dropstop')
                self.happy_gif.close()
                self.start_audio('dropstop')
                self.product_page_audio_stop_cb()
                if self.product_page_audio_stop_cb() == "product-home-button":
                    self.current_process = 2
                    break
                self.product_page_change()

                self.happy_gif.open()
                # self.navigate_with_position('grophesense')
                self.happy_gif.close()
                self.start_audio('grophesense')
                self.product_page_audio_stop_cb()
                if self.product_page_audio_stop_cb() == "product-home-button":
                    self.current_process = 2
                    break
                self.product_page_change()

                self.happy_gif.open()
                # self.navigate_with_position('smartpen')
                self.happy_gif.close()
                self.start_audio('smartpen')
                self.product_page_audio_stop_cb()
                if self.product_page_audio_stop_cb() == "product-home-button":
                    self.current_process = 2
                    break
                self.product_page_change()

                self.happy_gif.open()
                # self.navigate_with_position('miniprojector')
                self.happy_gif.close()
                self.start_audio('miniprojector')
                self.product_page_audio_stop_cb()
                if self.product_page_audio_stop_cb() == "product-home-button":
                    self.current_process = 2
                    break
                self.product_page_change()

                self.happy_gif.open()
                # self.navigate_with_position('rollr')
                self.happy_gif.close()
                self.start_audio('rollr')
                self.product_page_audio_stop_cb()
                if self.product_page_audio_stop_cb() == "product-home-button":
                    self.current_process = 2
                    break
                self.product_page_change()

                self.happy_gif.open()
                # self.navigate_with_position('keyboard')
                self.happy_gif.close()
                self.start_audio('keyboard')
                self.product_page_audio_stop_cb()
                if self.product_page_audio_stop_cb() == "product-home-button":
                    self.current_process = 2
                    break
                self.product_page_change()

                self.happy_gif.open()
                # self.navigate_with_position('solar')
                self.happy_gif.close()
                self.start_audio('solar')
                self.product_page_audio_stop_cb()
                if self.product_page_audio_stop_cb() == "product-home-button":
                    self.current_process = 2
                    break
                self.product_page_change()

                self.happy_gif.open()
                # self.navigate_with_position('blue_globe')
                self.happy_gif.close()
                self.start_audio('blue_globe')
                self.product_page_audio_stop_cb()
                if self.product_page_audio_stop_cb() == "product-home-button":
                    self.current_process = 2
                    break
                self.product_page_change()

                self.happy_gif.open()
                # self.navigate_with_position('ztylus')
                self.happy_gif.close()
                self.start_audio('ztylus')
                self.product_page_audio_stop_cb()
                if self.product_page_audio_stop_cb() == "product-home-button":
                    self.current_process = 2
                    break
                self.product_page_change()

                return

    # 4 TEAM MEMBER PAGE
    def team_member(self):
        print("team member fun")
        self.button_pressed = ''

        while not rospy.is_shutdown():

            if self.button_pressed == "brijesh-button":
                print("gif open")
                self.happy_gif.open()
                self.navigate_with_position('brijesh')
                self.happy_gif.close()
                print('I am brijesh')
                self.start_audio('reached_destination')
                # self.return_to_home()
                return

            if self.button_pressed == "prasad-button":
                self.happy_gif.open()
                time.sleep(4)
                self.navigate_with_position('prasad')
                self.happy_gif.close()
                print("I am prasad")
                self.start_audio('reached_destination')
                return

            if self.button_pressed == "sujith-button":
                self.happy_gif.open()
                time.sleep(2)
                self.navigate_with_position('sujith')
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

    # 5 FAB LAB SUPPORT PAGE
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

    # 6 GEMBA PAGE
    def gemba(self):

        self.button_pressed = ""

        while not rospy.is_shutdown():

            if self.button_pressed == "gamba-back-button":
                self.current_process = 2
                return

    # 7 ELECTRICAL AND ELECTRONICS SUPPORT PAGE
    def eletrical_and_electronics_support(self):

        self.button_pressed = ''

        while not rospy.is_shutdown():

            if self.button_pressed == "chandan-button":
                print('I am chandan')
                return

            if self.button_pressed == "ele-back-button":
                self.current_process = 5
                return

    # 8 MECHANICAL SUPPORT PAGE

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

    # 9 FABRICATIO SUPPORT PAGE

    def fabrication_support(self):
        self.button_pressed = ''

        while not rospy.is_shutdown():

            if self.button_pressed == "sujith-button":
                print('I am sujith')
                return

            if self.button_pressed == "fabricatin-back-button":
                self.current_process = 5
                return

    # PROCESS FLOW STARTS HERE
    def main_process(self):
        self.current_process = 0

        while not rospy.is_shutdown():
            time.sleep(1)

            print(self.current_process)
            self.led_color(b=150)

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
                self.back_skip_2()

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

            elif self.current_process == 10:
                print(self.current_process)
                self.creative_lab_tour()


# MAIN
if __name__ == '__main__':
    rospy.init_node("main_flow", anonymous=True)
    test = flow()
    test.main_process()
