import rospy
from std_msgs.msg import String
from arduino_serial.msg import RGBColor

pub = rospy.Publisher("/led_control", RGBColor, queue_size=10)

def mood_light_callback(data):
    if data.data == "red":
        color = RGBColor()
        color.R = 180
        color.G = 0
        color.B = 0
        color.T = 0
        pub.publish(color)
    

    elif data.data == "green":
        color = RGBColor()
        color.R = 0
        color.G = 180
        color.B = 0
        color.T = 0 
        pub.publish(color)

    elif data.data == "blue":
        color = RGBColor()
        color.R = 0
        color.G = 0
        color.B = 180
        color.T = 0 
        pub.publish(color)

    elif data.data == "black":
        color = RGBColor()
        color.R = 0
        color.G = 0
        color.B = 0
        color.T = 0 
        pub.publish(color)
             


if __name__ == '__main__':
    rospy.init_node("led_listner", anonymous=True)
    rospy.Subscriber('/mood_light', String, mood_light_callback)
    rospy.spin()


    