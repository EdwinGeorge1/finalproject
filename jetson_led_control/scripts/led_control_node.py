#! /usr/bin/env python

# dev notes:
# created by Arthur Gomes
# for controlling WS2812b LEDs over SPI connection with jetson nano. (works on RPI also)

import rospy 
import board
import neopixel_spi as neopixel
from jetson_led_control.msg import RGBColor

class ROS_spi_led_control:

    def __init__(self, nodeName):

        rospy.init_node(nodeName)

        numberOfLEDs = rospy.get_param("~LED_number", 10)
        topicName = rospy.get_param("~topic_name", '/led_control')
        rospy.Subscriber(topicName, RGBColor, self.callback)

        self.spi = board.SPI()
        self.ledHandle = neopixel.NeoPixel_SPI(self.spi, numberOfLEDs, pixel_order=neopixel.GRB, auto_write=False, frequency=6400000)
        for i in range(10):
            self.ledHandle.fill(0x000000)
            self.ledHandle.show()
        rospy.loginfo("LED control Node setup complete. subscribed to " + topicName)

    def callback(self, msg):

        color = (msg.R << 16) + (msg.G << 8) + (msg.B)
        rospy.loginfo("SSSSSetting color to:{},{},{}".format(msg.R, msg.G, msg.B))
        self.ledHandle.fill(color)
        self.ledHandle.show()

if __name__ == '__main__':

    ledNode = ROS_spi_led_control('led_control_node')
    rospy.spin()
    rospy.loginfo("node shutting down")