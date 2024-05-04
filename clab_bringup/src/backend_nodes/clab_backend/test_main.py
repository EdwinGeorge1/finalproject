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
import os

# OUR OWN MODULES IMPORTS
from gestureControl import gestureControl
from GifDisplay import GifDisplay

# ENABLE THIS SO THAT ARMS CAN WORK
gestureControl.ARMS_ENABLE = True
gestureControl.HEAD_ENABLE = True

# PYGAME INITIALIZING FOR PLAYING AUDIO
pygame.init()
pygame.mixer.init()


# INITIALIZING CLASS

class flow():
    def __init__(self):

        """
        This is the main script for clab robot. 

        Author: Sriram Arumugam.

        Co-author: Aroop Josy.

        Usage: "rosrun clab_bringup clab.py"

        # Hand and Head Movements: 
        Start :
            gestureControl.ARMS_ENABLE = True
            gestureControl.HEAD_ENABLE = True

        Stop:
            gestureControl.ARMS_ENABLE = False
            gestureControl.HEAD_ENABLE = False

        # Reading the Code:
            Go Down to this class method called main_flow() start reading from there.

        """

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

        # PUBLISHER FOR BRINGING UP SAD IMAGE
        self.sad_gif_publisher = rospy.Publisher("/open_sad_gif", Float32, queue_size=1)

        # ROS SUBSCRIBERS

        # NAV RESULT SUB
        rospy.Subscriber('/way_cmp', String, self.nav_cb, queue_size=1)

        # BUTTON FEEDBACK SUB
        rospy.Subscriber('/button', String, self.button_cb, queue_size=1)

        # LIDAR FEEDBACK SUB
        rospy.Subscriber('/wakeup_lidar', Bool, self.blank_screen_cb)
        self.battery_voltage_sub = rospy.Subscriber('/battery_voltage', Float32, self.battery_callback, queue_size=1)
        rospy.Subscriber("/joy", Joy, self.joy_cb, queue_size=1)

        # ATTRIBUTES NEEDED FOR METHODS
        self.current_process = 0
        self.nav_result = ""
        self.navigating = False

        # CREATING OBJECT FOR GIF DISPLAY CLASS
        self.happy_gif = GifDisplay('/home/jetson/clab_ws/src/clab/gif_files/happy.mp4')
        self.sad_gif = GifDisplay('/home/jetson/clab_ws/src/clab/gif_files/sad.mp4')


#CREATING OBJECT FOR GESTURE CONTROL CLASS 
        self.gesture_control = gestureControl()

    def arm_op_nd_cls(self, duration, home = 0.8, away = 1.2):

        self.gesture_control_up = gestureControl(arms_limits=(home, away))
        self.gesture_control_up.start(duration)



        # ALL THE GOAL POSITIONS SHOULD BE MENTIONED HERE BEFORE CALLING THEM

        self.goals = {"home": {"x": 0.6916, "y": 2.1305, "z": 0.3809, "w": 0.9245},

                      "brijesh": {"x": 1.4209, "y": -2.416, "z": -0.6081, "w": 0.7938},

                      "prasad": {"x": 0.0227, "y": 4.3203, "z": -0.9265, "w": 0.3760},

                      "sujith": {"x": 1.2420, "y": 3.0878, "z": -0.3649, "w": 0.9310},

                      "chandan": {"x": 1.8873, "y": 2.2822, "z": 0.9369, "w": 0.3493},

                      "spirestone": {"x": -0.6869, "y": 4.9093, "z": -0.3832, "w": 0.9236},

                      "wemoswitch": {"x": -0.0818, "y": 3.1142, "z": 0.4006, "w": 0.9162},

                      "dropstop": {"x": 3.1365, "y": 0.8126, "z": -0.0354, "w": 0.9993},

                      "1": {"x": 7.5741, "y": 4.4646, "z": 0.3899, "w": 0.9208},

                      "2": {"x": 7.0370, "y": 4.5696, "z": -0.9150, "w": 0.4033},

                      "3": {"x": 7.3272, "y": 4.0186, "z": -0.9210, "w": 0.3895},

                      "4": {"x": 6.8683, "y":  3.6529, "z": -0.9194, "w": 0.3931},

                      "5": {"x": 6.5911, "y": 3.3458, "z": -0.9195, "w": 0.3929},

                      "6": {"x": 6.2983, "y": 3.0227, "z": -0.9192, "w": 0.3935},

                      "7": {"x": 6.0209, "y": 2.7321, "z": -0.9192, "w": 0.3937},

                      "8": {"x": 5.7131, "y": 2.3756, "z": -0.9193, "w": 0.3935},

                      "9": {"x": 5.1745, "y": 1.7783, "z": -0.9174, "w": 0.3977},

                      "10": {"x": 4.6900, "y": 1.3046, "z": -0.9193, "w": 0.3935},

                      "11": {"x": 4.07977, "y": 0.6817, "z": -0.9153, "w": 0.4027},

                      "12": {"x": 3.6579, "y": 0.3228, "z": -0.9137, "w": 0.4062},

                      "13": {"x": 3.1997, "y": -0.2234, "z": -0.9126, "w": 0.4086},

                      "14": {"x": 2.7882, "y": -0.6709, "z": -0.9064, "w": 0.4223},

                      "15": {"x": 1.5589, "y": 1.2315, "z": -0.9100, "w": 0.4144},

                      "16": {"x": 0.5843, "y": 2.9858, "z": -0.9121, "w": 0.4097},

                      "17": {"x": 0.2872, "y": 3.8878, "z": 0.4035, "w": 0.9149},

                      "18": {"x": -1.3534, "y": 3.6140, "z": 0.3850, "w": 0.9228},

                      "19": {"x": -0.3742, "y": 3.0286, "z": -0.9126, "w": 0.4087},

                      "20": {"x": -0.5637, "y": 2.4639, "z": -0.9115, "w": 0.4112},

                      "21": {"x": -1.022, "y": 1.9665, "z": -0.9108, "w": 0.4126},

                      "22": {"x": -1.4407, "y": 3.5225, "z": -0.9088, "w": 0.4170},

                      "23": {"x": -0.9432, "y": 3.0798, "z": -0.9148, "w": 0.4038},

                      }
              

        self.person_in_range = False  #Flag for Lidar

        self.checK_img_open = False

        self.exhibition_one_tour = False

        self.exhibition_two_tour = False
        

    # THIS CALLBACK METHOD WAKES THE SCREEN ON
    def blank_screen_cb(self, data):

        self.one_meter_range = data.data
        
        if self.one_meter_range == False:
            self.person_in_range = False
            return 
        
        if self.one_meter_range == True:
            self.person_in_range = True
            # self.close_image()
            return 
            
  
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
        
        if self.voltage < 11:
            self.sad_gif.open()
            self.battery_voltage_sub.unregister()

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
    

    #THIS METHOD GIVES US THE EXACT EXIHIBITION SELECTED BY THE USER FOR TOUR
    def file_reader(self):
        file_reader = open(r"/var/www/html/clab/data.txt", "r")

        self.exh_type = file_reader.readline()

        return self.exh_type

    # THIS CALLBACK METHOD CHECKS FOR NAV RESULT
    def nav_cb(self, data):
        self.nav_result = data.data

    # THIS CALLBACK METHOD GIVES THE BUTTON PRESSED FEEDBACK FROM UI
    def button_cb(self, data):
        dict1 = json.loads(data.data)
        print("button data")
        print(dict1)
        self.button_pressed = dict1["button"]
        if self.button_pressed == "switchoff_button":
            os.system("sh /home/jetson/clab_ws/src/clab/clab_bringup/src/led_off.sh")       #to turnoff the led_strips
            os.system("sudo /home/jetson/clab_ws/src/clab/clab_bringup/src/./shutdown.sh")  #to shutdown the whole system

    # THIS METHOD IS OPEN IMAGE FILE WHEN NEEDED
    def open_image(self, name):
        self.checK_img_open = True
        call('sh /home/jetson/clab_ws/src/clab/clab_bringup/src/show_image.sh ' + name, shell=True)
        

    # THIS METHOD IS CLOSE IMAGE FILE WHEN NEEDED
    def close_image(self):
        self.checK_img_open = False
        call('sh /home/jetson/clab_ws/src/clab/clab_bringup/src/close_image.sh', shell=True)

    # THIS METHOD IS TO START AUDIO ALONG WITH HAND AND HEAD GESTRUE
    def start_audio(self, audio_name):

        duration = self.check_audio_timing(audio_name)
        pygame.mixer.music.load('/home/jetson/clab_ws/src/clab/audios/' + audio_name + '.mp3')
        print(audio_name)
        pygame.mixer.music.play()
        # self.gesture_control.setHead("home")
        # self.gesture_control.start(duration)
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

    def show_gif(self, name):
        call('sh /home/jetson/clab_ws/src/clab/clab_bringup/src/show_gif.sh ' + name, shell=True)

    # THIS METHOD IS CLOSE GIF FILE WHEN NEEDED

    def close_gif(self):
        call('sh /home/jetson/clab_ws/src/clab/clab_bringup/src/close_gif.sh', shell=True)

# BELOW TWO METHOD SERVES PRODUCT PAGE

    # THIS METHOD CHECKS FOR BUTTON FEEDBACK, AND STOPS AUDIO AND HELPS BREAKING LOOP
    def product_page_audio_stop_cb(self):
        
        while pygame.mixer.music.get_busy():
            print("busy")
            if self.button_pressed == 'product_home_button':
                self.stop_audio()
                return self.button_pressed
            
            if self.button_pressed == "home_button":
                self.stop_audio()
                return self.button_pressed
            
            if self.button_pressed == "product_prev_button":
                pygame.mixer.music.pause()
                print("i am paused")
                self.resume()
                break

        return self.button_pressed
    
    def resume(self):
        resume_flag = False

        while resume_flag == False:
            print("i m in resume method")

            if self.button_pressed == "product_next_button":
                pygame.mixer.music.unpause()
                self.product_page_audio_stop_cb()
                break

            if self.button_pressed == "product_home_button":
                break

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

#THIS METHOD STOP AND RESUMES THE PRODUCT PAGE AS WELL AS WHOLE LAB TOUR
    def pause_and_resume(self):

        self.button_pressed = " "

        exit_time = time.time() + 15

        while self.pause == True:

            if time.time() > exit_time and self.button_pressed == " " :
                self.pause = False
                break
            
            if self.button_pressed == "pause":
                print("paused")
                
            if self.button_pressed == "play":
                print("resumed")
                self.pause = False
                break

            if self.button_pressed == "home_button":
                self.current_process = 2
                break

        return self.pause

    def product_name(self, audio_name):
        self.gesture_control.setHead("left_nod")
        self.start_audio(audio_name)
        self.product_page_audio_stop_cb()
        self.gesture_control.setHead("home")


    #EXHIBITION ONE FOR PRODUCT PAGE AND CLAB TOUR
    def exhibition_one(self):

        while self.exhibition_one_tour == True :

            self.stop_audio()
            self.happy_gif.open()
            # self.navigate_with_position('13')
            self.happy_gif.close()
            self.product_name("spirestone_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('spirestone')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            # if self.product_page_audio_stop_cb() == "product_prev_button":
                # self.resume()

            # self.pause = True
            # self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            # self.navigate_with_position('5')
            self.happy_gif.close()
            self.product_name("belkin_wemo_switch_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('wemoswitch')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            # self.navigate_with_position('12')
            self.happy_gif.close()
            self.product_name("drop_stop_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('dropstop')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('7')
            self.happy_gif.close()
            self.product_name("grohe_sense_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('grophesense')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('8')
            self.happy_gif.close()
            self.product_name("smart_pen_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('smartpen')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('9')
            self.happy_gif.close()
            self.product_name("mini_projector_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('miniprojector')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('10')
            self.happy_gif.close()
            self.product_name("rollr_mini_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('rollr')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('11')
            self.happy_gif.close()
            self.product_name("keyboard_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('keyboard')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('12')
            self.happy_gif.close()
            self.product_name("solar_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('solar')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('13')
            self.happy_gif.close()
            self.product_name("blue_globe_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('blue_globe')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('14')
            self.happy_gif.close()
            self.product_name("ztylus_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('ztylus')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()
            self.exhibition_one_tour = False

        return 
    
    # EXHIBITION TWO FOR PRODUCT PAGE AND CLAB WHOLE TOUR
    def exhibition_two(self):

        while self.exhibition_two_tour == True :

            self.stop_audio()
            self.happy_gif.open()
            self.navigate_with_position('14')
            self.happy_gif.close()
            self.product_name("battery_cooling_system_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('batterycoolingsystem')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('15')
            self.happy_gif.close()
            self.product_name("ac_vent_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('air_conditioning')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('6')
            self.happy_gif.close()
            self.product_name("car_door_knob_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('car_door_knob')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('7')
            self.happy_gif.close()
            self.product_name("reflector_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('reflector')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('8')
            self.happy_gif.close()
            self.product_name("chamber_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('chamber_plenum')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('9')
            self.happy_gif.close()
            self.product_name("voxels_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('voxels')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('10')
            self.happy_gif.close()
            self.product_name("ultrasint_tpu_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('ultrsint_tpu')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('11')
            self.happy_gif.close()
            self.product_name("automotive_gear_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('automotive_gear')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('12')
            self.happy_gif.close()
            self.product_name("power_steering_joint_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('power_steering_joint')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('13')
            self.happy_gif.close()
            self.product_name("fuel_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('fuel_swirler')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()

            self.happy_gif.open()
            self.navigate_with_position('14')
            self.happy_gif.close()
            self.product_name("medical_ns")
            self.gesture_control.moveHand(1.09)
            self.start_audio('medical_device')
            self.product_page_audio_stop_cb()
            self.gesture_control.moveHand()
            if self.product_page_audio_stop_cb() == "product_home_button":
                self.current_process = 11
                break
            self.pause = True
            self.pause_and_resume()
            self.product_page_change()
            self.exhibition_two_tour = False

        return self.current_process
    
    def pls_follow_me(self):
        self.start_audio("please_follow_me") 
        self.arm_limits(1, 0.8, 1.8)
        self.gesture_control.setHead("right_nod")
        time.sleep(0.5)
        self.gesture_control.setHead("home")

    def nod_movement(self, required_movement):
        
        self.gesture_control.setHead(required_movement)
        time.sleep(0.5)
        self.gesture_control.setHead("home")

    # BELOW METHODS ARE THE MAIN PROCESS

    # 0 START PAGE
    def home_page(self):

        self.button_pressed = ''
        
        wait_time = time.time() + 120

        while not rospy.is_shutdown():

            if self.button_pressed == "start-button":
                # self.launch_start.publish('fablab_intro')
                self.start_audio("hello")
                self.nod_movement("down")
                self.arm_op_nd_cls(1,0.8,1.09)
                self.current_process = 1
                return
            
            if time.time() > wait_time and self.person_in_range == False:
                self.open_image("blank.png")
                return
            
            if self.person_in_range == True and self.checK_img_open == True:
                wait_time = time.time() + 5
                self.close_image()
                return
            
    # 1 BACK_SKIP PAGE

    def back_skip(self):

        wait_time = time.time() + 30
        self.button_pressed = ''

        while not rospy.is_shutdown():

            if time.time() > wait_time:
                print('go to home position')
                self.launch_start.publish("")
                self.current_process = 0
                return
             
            if self.button_pressed == "video-back-button":
                self.stop_audio()
                print("bk pressed")
                self.current_process = 0
                return

            if self.button_pressed == "video-skip-button":
                self.stop_audio()
                print("skip_pressed")
                self.start_audio('please_choose')
                self.current_process = 2
                return

    # 2 OPTIONS SHOWING PAGE

    def options_showing(self):
        print("option showing")
        wait_time = time.time() + 120
        self.button_pressed = ''
        while not rospy.is_shutdown():

            if self.button_pressed == "creative-option-button":
                self.stop_audio()
                print("clab")
                # self.start_audio('creative_lab_tour')
                self.current_process = 11
                return

            if self.button_pressed == "clab-team-member":
                print("team members")
                self.stop_audio()
                self.start_audio('willguideyou')
                print("after start_audio")
                self.current_process = 4
                return

            if self.button_pressed == "fablab-button":
                self.stop_audio()
                self.start_audio('willguideyou')
                self.current_process = 12
                return

            if self.button_pressed == "gimba-button":
                self.current_process = 6
                return
            
            if time.time() > wait_time:
                print('go to home position')
                self.launch_start.publish("start")
                self.navigate_with_position("home")
                self.current_process = 0
                return
            
    # 11 Creative lab options        

    def creative_lab_options(self):
        
        print("creative_lab_options")
        self.button_pressed = ""

        while not rospy.is_shutdown():

            if self.button_pressed == "about-creative-button":
                self.start_audio("hello")
                self.current_process = 3
                return
            
            if self.button_pressed == "exhibition-one-button":
                self.current_process = 10
                return
            
            if self.button_pressed == "exhibition-two-button":
                self.current_process = 13
                return
            
            if self.button_pressed == "creative_option_back_button":
                self.current_process = 2
                return
                

    # 3 BACK SKIP PAGE 2

    def back_skip_2(self):
        self.button_pressed = ""

        while not rospy.is_shutdown():


            if self.button_pressed == "about-creative-back-button":
                self.stop_audio()
                self.current_process = 11
                return


    # 10 CREATIVE LAB EXHIBITION ONE TOUR STARTS HERE
    def creative_lab_tour(self):

        while not rospy.is_shutdown():

            if self.button_pressed == "exhibition-one-button":
                self.exhibition_one_tour = True
                self.exhibition_one()
                return
            
    # 13 CREATIVE LAB EXHIBITION TWO TOUR STARTS HERE         
    def creative_lab_tour_2(self):

        while not rospy.is_shutdown():

            if self.button_pressed == "exhibition-two-button":
                self.exhibition_two_tour = True
                self.exhibition_two()
                if self.exhibition_two() == 2:
                    self.current_process = 11

                else:
                    self.launch_start.publish("start")
                    self.current_process = 0

                return

    # 4 TEAM MEMBER PAGE
    def team_member(self):
        print("team member fun")

        wait_time = time.time() + 60
        self.button_pressed = ''

        while not rospy.is_shutdown():
            # print(wait_time)

            if time.time() > wait_time:
                print('go to home position', time.time())
                self.navigate_with_position('home')
                self.launch_start.publish("start")
                self.current_process = 0
                return

            if self.button_pressed == "brijesh_button":
                self.nod_movement("down")
                print("gif open")
                self.happy_gif.open()
                self.navigate_with_position('15')
                self.happy_gif.close()
                print('I am brijesh')
                self.start_audio('reached_destination')
                wait_time = time.time() + 60
                # self.return_to_home()
                return

            if self.button_pressed == "deepak_button":
                self.nod_movement("down")
                self.happy_gif.open()
                time.sleep(4)
                self.navigate_with_position('16')
                self.happy_gif.close()
                print("I am deepak")
                self.start_audio('reached_destination')
                wait_time = time.time() + 60
                return

            if self.button_pressed == "vamshi_button":
                self.nod_movement("down")
                self.happy_gif.open()
                time.sleep(2)
                self.navigate_with_position('17')
                self.happy_gif.close()
                print("I am vamshi")
                self.start_audio('reached_destination')
                wait_time = time.time() + 60
                return

            if self.button_pressed == "ambadi_button":
                self.nod_movement("down")
                self.happy_gif.open()
                time.sleep(2)
                self.navigate_with_position('18')
                self.happy_gif.close()
                print("I am ambadi")
                self.start_audio('reached_destination')
                wait_time = time.time() + 60
                return

            if self.button_pressed == "bharathwaaj_button":
                self.nod_movement("down")
                self.navigate_with_position('19')
                print("I am bharathwaaj")
                self.start_audio('reached_destination')
                return

            if self.button_pressed == "back_button":
                # self.navigate_with_position('21')
                # self.call_startpage()
                self.current_process = 2
                return

    # 12 fab_lab_button            
    
    def fab_lab_button(self):
        self.button_pressed = ""
        
        while not rospy.is_shutdown():

            if self.button_pressed == "fablab-intro-button":
                self.start_audio("hello")
                # self.current_process = 2
                return

            if self.button_pressed == "fablab-support-button":
                self.current_process = 5
                return
            
            if self.button_pressed == "fablab_option_back_button":
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

            if self.button_pressed == "fablab-support-back-button":
                self.current_process = 12
                return
            
    def gemba(self):
        while not rospy.is_shutdown():

            if self.button_pressed == "gimba-button":

        #ABOUT CREATIVE LAB HAS TWO SESSIONS 

            # #1 ->  NETWORK_BOARD
                self.stop_audio()
                self.happy_gif.open()
                self.navigate_with_position('20')
                self.happy_gif.close()
                self.launch_start.publish("network_board")
                self.start_audio("network_board")
                self.nod_movement("down")
                self.gesture_control.moveHand(1.09)
                self.product_page_audio_stop_cb()
                self.gesture_control.moveHand()
                if self.product_page_audio_stop_cb() == "home_button":
                    self.current_process = 2
                    break
                self.pause = True
                self.pause_and_resume()

            # #2 -> NEAR_POSTER
                self.happy_gif.open()
                self.navigate_with_position('20')
                self.happy_gif.close()
                self.launch_start.publish("near_poster")
                self.start_audio("near_poster")
                self.nod_movement("down")
                self.gesture_control.moveHand(1.09)
                self.product_page_audio_stop_cb()
                self.gesture_control.moveHand()
                if self.product_page_audio_stop_cb() == "home_button":
                    self.current_process = 2
                    break
                self.pause = True
                self.pause_and_resume()

            # IF EXHIBITION_ONE IS SELECTED FLOW GOES TO THIS BLOCK BELOW

                if self.file_reader() == "exhibition_one":
                    self.launch_start.publish("exhibition_one")
                    self.exhibition_one_tour = True
                    self.exhibition_one()
                    if self.current_process == 11:
                        self.launch_start.publish("option_showing")
                        self.current_process = 2
                        break

            # IF EXHIBITION_TWO IS SELECTED FLOW GOES TO THIS BLOCK BELOW

                if self.file_reader() == "exhibition_two":
        
                    self.launch_start.publish("exhibition_two")
                    self.exhibition_two_tour = True
                    self.exhibition_two()
                    if self.current_process == 11:
                        self.launch_start.publish("option_showing")
                        self.current_process = 2
                        break


            # COLLABRATIVE SPACE
                self.happy_gif.open()
                self.launch_start.publish("colaburative_space")
                self.navigate_with_position('22')
                self.happy_gif.close()
                self.start_audio("collaborative")
                self.nod_movement("down")
                self.gesture_control.moveHand(1.09)
                self.product_page_audio_stop_cb()
                self.gesture_control.moveHand()
                if self.product_page_audio_stop_cb() == "home_button":
                    self.current_process = 2
                    break
                self.pause = True
                self.pause_and_resume()


            #FAB LAB INTRO
                self.happy_gif.open()
                self.launch_start.publish("fablab_intro")
                self.navigate_with_position('19')
                self.happy_gif.close()
                self.start_audio("fab_intro")
                self.nod_movement("down")
                self.gesture_control.moveHand(1.09)
                self.product_page_audio_stop_cb()
                self.gesture_control.moveHand()
                if self.product_page_audio_stop_cb() == "home_button":
                    self.current_process = 2
                    break
                self.pause = True
                self.pause_and_resume()

                self.launch_start.publish("start")
                time.sleep(0.5)
                self.current_process = 0

                return

    # 7 ELECTRICAL AND ELECTRONICS SUPPORT PAGE
    def eletrical_and_electronics_support(self):

        self.button_pressed = ''

        while not rospy.is_shutdown():

            if self.button_pressed == "ambadi-button":
                print('I am ambadi')
                return

            if self.button_pressed == "ele-back-button":
                self.current_process = 5
                return

    # 8 MECHANICAL SUPPORT PAGE

    def mechanical_support(self):

        self.button_pressed = ''

        while not rospy.is_shutdown():

            if self.button_pressed == "sujith-button":
                print('I am Bharatwaj')
                return

            if self.button_pressed == "mech-back-button":
                self.current_process = 5
                return

    # 9 FABRICATION SUPPORT PAGE

    def fabrication_support(self):
        self.button_pressed = ''

        while not rospy.is_shutdown():

            if self.button_pressed == "bharatwaaj-button":
                print('I am bharatwaaj')
                return
 
            if self.button_pressed == "fabrication-back-button":
                self.current_process = 5
                return

    # PROCESS FLOW STARTS HERE
    def main_process(self):
        self.current_process = 11
        self.arm_op_nd_cls(1.5,0.8,1.28)

        while not rospy.is_shutdown():
            # time.sleep(1)

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

            elif self.current_process == 11:
                print(self.current_process)
                self.creative_lab_options()

            elif self.current_process == 12:
                print(self.current_process)
                self.fab_lab_button()

            elif self.current_process == 13:
                print(self.current_process)
                self.creative_lab_tour_2()


# MAIN
if __name__ == '__main__':
    rospy.init_node("main_flow", anonymous=True)
    clab = flow()
    clab.main_process()


    # calb.start_audio("hello")
    # time.sleep(2)
    # pygame.mixer.music.pause()
    # time.sleep(2)
    # pygame.mixer.music.unpause()
    # time.sleep(10)