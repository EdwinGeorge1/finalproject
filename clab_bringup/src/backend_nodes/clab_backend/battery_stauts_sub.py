import rospy
from std_msgs.msg import Float32




def callback(data):
    voltage = data.data

    if voltage < 10:
        print("low_battery")

if __name__ == '__main__':
    rospy.init_node("battery_listner", anonymous=True)
    rospy.Subscriber('/battery_voltage', Float32, callback)
    rospy.spin()


    