#!/bin/sh
gnome-terminal --tab -e "bash -c \"roslaunch openni_launch openni.launch  depth_registration:=true;exec bash\"" \
--tab -e "bash -c \"cd ~/catkin_ws/src/depth/scripts;source ~/tensorflow/bin/activate;rosrun depth kinect_detect.py;exec bash\"" \
--tab -e "bash -c \"sleep 20s;rosrun depth depth_kinect.py;exec bash\"" \
--tab -e "bash -c \"echo -e \" \" | sudo -S service ssh status -\ ;exec bash\"" \
--tab -e "bash -c \"cd ~/Desktop/RMI/Controller;java -jar AioRemoteDesktop3.5.0.jar;exec bash\"" \
--tab -e "bash -c \"sleep 10s;rosrun pepper Odom_publish.py;exec bash\"" \
--tab -e "bash -c \"sleep 10s;rosrun pepper graph.py;exec bash\"" \
--tab -e "bash -c \"sleep 10s;cd ./Desktop/RMI/Codes/;python controller.py;exec bash\""


: '
Launch 
roslaunch openni_launch openni.launch  depth_registration:=true

roscd depth/scripts/
source ~/tensorflow/bin/activate 
rosrun depth kinect_detect.py 

rosrun depth depth_kinect.py 

sudo service ssh status


cd ~/Desktop/RMI/Controller
java -jar AioRemoteDesktop3.5.0.jar 


rosrun pepper Odom_publish.py

rosrun pepper graph.py 




cd ./Desktop/RMI/Codes/
python controller.py
'