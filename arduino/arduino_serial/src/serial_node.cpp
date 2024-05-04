#include <ros/ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Float32.h>
#include "arduino_serial/RGBColor.h"

#include <serial/serial.h>
#include <chrono>
#include <thread>
#include <string>

serial::Serial *serialPtr;

void callback(const arduino_serial::RGBColor& color)
{
  unsigned char message[7];
  message[0] = '#';
  message[1] = color.R;
  message[2] = color.G;
  message[3] = color.B;
  message[4] = color.T >> 8; //MSB
  message[5] = color.T & 0xFF; //LSB
  message[6] = '\n';
  
  serialPtr->write(message,7);
  
  ROS_INFO("sent message");
}

int main(int argc, char** argv) {

  //init ROS
  ros::init(argc, argv, "serial_node");
  ros::NodeHandle nh;

  //read serial port and baud from param server
  if(!ros::param::has("~port")){
      ROS_ERROR("private param <port> not found.");
      ros::shutdown();
      return -1;
  }
  if(!ros::param::has("~baud")){
      ROS_ERROR("private param <baud> not found");
      ros::shutdown();
      return -1;
  }

  std::string port, led_control_topic, battery_voltage_topic;
  int baud;
  ros::param::get("~port", port);
  ros::param::get("~baud", baud);

  // Initialize serial port
  serial::Serial temp(port, baud, serial::Timeout::simpleTimeout(500));

  if(!temp.isOpen()){
    ROS_ERROR("failed to open serial port");
    return -1;
  }

  //spam test messages
  for(int i =0; i<5; i++){
    temp.write("test\0");
  }

  serialPtr = &temp;
  ros::Publisher pub = nh.advertise<std_msgs::Float32>("/battery_voltage", 1);
  ros::Subscriber sub = nh.subscribe("/led_control", 5, callback);

  ROS_INFO("node setup complete");
  while(ros::ok())
  {
    try 
    {
      std::string message = serialPtr->readline(10, "\n");

      if(message.length() > 0)
      {
        std_msgs::Float32 msg;
        msg.data = std::stof(message);
        pub.publish(msg);
      }
    } 
    catch (const std::invalid_argument& e) 
    {
      // handle error: stof failed to find a floating point value in the string
      std::cerr << "error: " << e.what() << std::endl;
    } 
    catch (const std::out_of_range& e) 
    {
      // handle error: stof found a valid floating point value, but it was too large or too small to represent as a float
      std::cerr << "error: " << e.what() << std::endl;
    }
    ros::spinOnce();
  }

  return 0;
}