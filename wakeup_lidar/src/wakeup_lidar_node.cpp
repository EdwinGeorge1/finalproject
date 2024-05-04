#include "ros/ros.h"
#include "sensor_msgs/LaserScan.h"
#include "std_msgs/Bool.h"

#include <vector>

//globals
ros::Publisher wakeupPub;
int prev_number = 0;
bool PREV_NUMBER_SET = false;
float wakeup_distance;
int wakeup_threshold;
int check_freq = 10;
int check_count = 0;


void callback(sensor_msgs::LaserScan::ConstPtr msgPtr)
{
    if(check_count < check_freq)
    {
        check_count++;
        return;
    }
    else
    {
        check_count=0;
    
        int current_number = 0;
        for(float range : msgPtr->ranges){
            if(range < wakeup_distance){
                current_number++;
            }
        }

        if(!PREV_NUMBER_SET){
            prev_number = current_number;
            PREV_NUMBER_SET = true;
            return;
        }
        //ROS_INFO_STREAM("current count "<< current_number << " t=" << wakeup_distance);

        
        if(current_number - prev_number > wakeup_threshold){
            ROS_INFO("detected movement towards robot");
            ROS_INFO("waiting for subscriber to connect");
            while(wakeupPub.getNumSubscribers() <= 0);
            std_msgs::Bool msg;
            msg.data = true;
            wakeupPub.publish(msg);
            
        }

        // else{
        //     ROS_INFO("No movement towards robot");
        //     ROS_INFO("waiting for subscriber to connect");
        //     while(wakeupPub.getNumSubscribers() <= 0);
        //     std_msgs::Bool msg;
        //     msg.data = false;
        //     wakeupPub.publish(msg);
        // }

        prev_number = current_number;
        return;
    }
}

int main(int argc, char** argv)
{

    ros::init(argc, argv, "wakeup_lidar_node");
    ros::NodeHandle nh;

    if(!ros::param::has("~wakeup_distance")){
        ROS_ERROR("private param <wakeup_distance> not found. (metres)");
        ros::shutdown();
        return 0;
    }

    if(!ros::param::has("~wakeup_threshold")){
        ROS_ERROR("private param <wakeup_threshold> not found");
        ros::shutdown();
        return 0;
    }

    if(!ros::param::has("~check_freq")){
        ROS_ERROR("private param <check_freq> not found. Perform a check once every x scans");
        ros::shutdown();
        return 0;
    }

    float tempA;
    int tempB, tempC;
    ros::param::get("~wakeup_distance", tempA);
    ros::param::get("~wakeup_threshold", tempB);
    ros::param::get("~check_freq", tempC);
    wakeup_distance = tempA;
    wakeup_threshold = tempB;
    check_freq = tempC;

	ROS_INFO_STREAM("distance "<< wakeup_distance << " threshold " << wakeup_threshold);
    ros::Subscriber laserSub = nh.subscribe("/scan", 5, callback);
    wakeupPub = nh.advertise<std_msgs::Bool>("/wakeup_lidar", 10);
	ROS_INFO("node setup complete");
    ros::spin();

    return 0;
}   
