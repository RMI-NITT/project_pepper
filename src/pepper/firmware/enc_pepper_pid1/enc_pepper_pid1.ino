#include<Encoder.h>
#include <ros.h>
#include <ros/time.h>
#include <geometry_msgs/PointStamped.h>
#define radius 0.0526
Encoder enc_R(2,3); //encoder input
Encoder enc_L(18,19);
int Left_motor_pwm = 9;
int Right_motor_pwm = 8;
int Left_dir = 23;  // HIGH is forward
int Right_dir = 22;

ros::NodeHandle  nh;
geometry_msgs::PointStamped msg;
ros::Publisher encoder("encoder", &msg);

void setup() {

  nh.initNode();
  nh.advertise(encoder);
  
  Serial.begin(115200);
  Serial.println("Basic Encoder Test:");

  //Motor Left
  pinMode(9,OUTPUT);  //PWM_L
  pinMode(18,INPUT);  //EncoderLB
  pinMode(19,INPUT);  //EncoderLA
  pinMode(23,OUTPUT); //DIR_L

  //Motor Right
  pinMode(22,OUTPUT); //DIR_R
  pinMode(8,OUTPUT);  //PWM_R
  pinMode(2,INPUT);   //EN_RA
  pinMode(3,INPUT);   //EN_RB
  
  //Set Test PWM
  analogWrite(Right_motor_pwm,100);
  analogWrite(Left_motor_pwm,100);
}

double cur_enc_L= 0,kp = 0.8, ki = 0.01, cur_enc_R= 0,prev_enc_l=0,err_l = 0,err_r=0,prev_enc_r=0,vel_l =0,vel_r=0,rpm_l = 100,rpm_r = 100,val_l=0.22,val_r=0.22;
void loop() {
  
  //Set Direction
  digitalWrite(Right_dir,HIGH);
  digitalWrite(Left_dir,HIGH);
    

  cur_enc_L = enc_L.read();
  cur_enc_R = enc_R.read();

  msg.header.stamp = nh.now();
  msg.header.frame_id = "world";
  msg.point.x = cur_enc_L;
  msg.point.y = cur_enc_R;
 
  // velocity = 2* 3.14* 0.052 * theta 
  
vel_l = ((cur_enc_L-prev_enc_l)*0.326)/(0.005*29520);
  vel_r =((cur_enc_R- prev_enc_r)*0.326)/(0.005*29520);
  err_l = val_l - vel_l;
  err_r = val_r - vel_r;
  
  //rpm_update
  
  rpm_l = rpm_l + err_l*kp;
  rpm_r = rpm_r + err_r*kp;
  analogWrite(Right_motor_pwm,rpm_l);
  analogWrite(Left_motor_pwm,rpm_r);
Serial.print(err_l);
Serial.print(' ');
Serial.println(vel_l);
  prev_enc_l = cur_enc_L;
  prev_enc_r = cur_enc_R;
  
  //Serial.print(vel_l);
  //Serial.print(' ');
  //Serial.println(vel_r);
  
  encoder.publish(&msg);
  nh.spinOnce();
  delay(5);
    
//  Serial.println(newpos);
  
}
