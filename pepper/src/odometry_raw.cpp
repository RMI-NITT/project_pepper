#include <ros/ros.h>
#include <string>
#include <geometry_msgs/PoseArray.h>
#include <sensor_msgs/JointState.h>
#include <tf/transform_broadcaster.h>
#include <geometry_msgs/Vector3.h>
#include <stdlib.h>

#define width_robot 0.30  //30cm distance between 2 wheels in mtrs
#define radius 0.05   // radius of the wheel in mtrs

class odometry
{
public:
	odometry();
private:
	ros::NodeHandle n;
	ros::Subscriber odom_sub;
	ros::Subscriber cmd_vel_sub;
	ros::Publisher vel_pub;
	void callback_odom(const geometry_msgs::Vector3::ConstPtr& num);
	void callback_cmd_vel(const geometry_msgs::Twist::ConstPtr& cmd_vel);				
};

void odometry::callback_odom (const geometry_msgs::Vector3::ConstPtr& num)
{
	ros::Rate loop_rate(20);
	tf::TransformBroadcaster broadcaster;		
	geometry_msgs::TransformStamped odom_tran;
	geometry_msgs::Quaternion odom_quat;
	ros::Time current_time;
	
	current_time = ros::Time::now();
	
	//update transform

	odom_quat = tf::createQuaternionMsgFromYaw(num->z); //calculate the quaternion from yaw assuming pitch and roll to be 0 deg
	odom_tran.header.frame_id = "odom";
	odom_tran.child_frame_id = "base_link";
	odom_tran.header.stamp = current_time;
	odom_tran.transform.translation.x = num->x;
	odom_tran.transform.translation.y = num->y;
	odom_tran.transform.translation.z = 0.0;
	odom_tran.transform.rotation = odom_quat;
	
	//broadcast 

	broadcaster.sendTransform(odom_tran);
	loop_rate.sleep();	
}

void odometry::callback_cmd_vel (const geometry_msgs::Twist::ConstPtr& cmd_vel)
{
	geometry_msgs::Vector3 motor_vel_msg; //msg to be published to the arduino
	
	double vel_x = cmd_vel->linear.x ;
	double vel_th = cmd_vel->angular.z;
	
	if (vel_x > 0.52)
		vel_x = 0.52;
	if (vel_th > 2)
		vel_th = 2;

	double vl = 0.0;
	double vr = 0.0;
	
	if(vel_x == 0)  //turning
	{
		vr = vel_th*width_robot/2.0;
		vl = (-1)*vr;
	}

	else if (vel_th == 0)  // moving FORWARD / backward
	{
		vr = vel_x;
		vl = vel_x;
	}
	else	//both	 
	{
		vr = vel_x + (vel_th * width_robot/2.0);
		vl = vel_x - (vel_th * width_robot/2.0);
	}

	vr = vr*9.5493/radius; //velocity to RPM conversion
	vl = vl*9.5493/radius;

	vr = vr*2.55;  //RPM to PWM conversion
	vl = vl*2.55;

	if (vr>255) 	
		vr = 255;
	if (vr<-255)
		vr = -255;
	if (vl>255)
		vl = 255;
	if (vl<-255)
		vl = -255;
	
	motor_vel_msg.x = vr;
	motor_vel_msg.y = vl;
	motor_vel_msg.z = 0;	

	vel_pub.publish(motor_vel_msg);	
}


odometry::odometry()
{
	
	odom_sub = n.subscribe<geometry_msgs::Vector3>("/odometry_raw", 100, &odometry::callback_odom,this);
	cmd_vel_sub = n.subscribe<geometry_msgs::Twist>("cmd_vel", 100, &odometry::callback_cmd_vel,this);
	vel_pub = n.advertise<geometry_msgs::Vector3>("motor_vel",100);
}

int main(int argc, char** argv)
{
ros::init(argc, argv, "odometry");
odometry k;
ros::spin();
}


	



