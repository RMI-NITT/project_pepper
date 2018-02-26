
#include <ros/ros.h>
#include <tf/transform_broadcaster.h>

int main(int argc, char** argv)
{
	ros::init(argc, argv , "tf_publisher");
	ros::NodeHandle n;
	ros::Rate r(100);
	tf::TransformBroadcaster broadcast;
	tf::Transform transform;
	
	while(n.ok())
	{	
		transform.setOrigin(tf::Vector3(0.1,0.0,0.2));
		transform.setRotation(tf::Quaternion(0,0,0,1));
		broadcast.sendTransform(tf::StampedTransform(transform,ros::Time::now(),"base_link","base_laser"));
		r.sleep();
	}
}


