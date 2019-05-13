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
  pinMode(8,OUTPUT);
  analogWrite(Right_motor_pwm,30);
  analogWrite(Left_motor_pwm,30);;  //PWM_R
  pinMode(2,INPUT);   //EN_RA
  pinMode(3,INPUT);   //EN_RB
  
  //Set Test PWM
  analogWrite(Right_motor_pwm,30);
  analogWrite(Left_motor_pwm,30);
}
double kil = 0,kir = 0,kpl = 0.031,kpr = 0.028; 
double cur_enc_L= 0, cur_enc_R= 0,prev_enc_l=0,prev_enc_r=0,err_l = 0,err_r=0,i_err_r =0,i_err_l=0,vel_l =0,vel_r=0,rpm_l = 30,rpm_r = 30,val_l=1,val_r=1;
void loop() {
  
  //Set Direction
  digitalWrite(Right_dir,HIGH);
  digitalWrite(Left_dir,HIGH  );
    

  cur_enc_L = enc_L.read();
  cur_enc_R = enc_R.read();

  msg.header.stamp = nh.now();
  msg.header.frame_id = "world";
  msg.point.x = cur_enc_L;
  msg.point.y = cur_enc_R;
 
  // velocity = 2* 3.14* 0.052 * theta *255/100
  
vel_l = ((cur_enc_L-prev_enc_l)*0.326*2.55)/(0.005*29520);
  vel_r =((cur_enc_R- prev_enc_r)*0.326*2.55)/(0.005*29520);
  err_l = val_l - vel_l;
  err_r = val_r - vel_r;
  i_err_l += err_l;
  i_err_r += err_r;
  //rpm_update
  if(abs(err_l) >0.05 || abs(err_r) > 0.05)
  {
  rpm_l = rpm_l + err_l*kpl + i_err_l*kil;//- 0.1*(vel_l - vel_r)/2;
  rpm_r = rpm_r + err_r*kpr+ i_err_r*kir ;//+ 0.1* (vel_l - vel_r)/2;
  }
  rpm_l = 50;
  rpm_r = 50;
  
  analogWrite(Right_motor_pwm,rpm_l);
  analogWrite(Left_motor_pwm,rpm_r);
//Serial.print(vel_r);
//Serial.print(' ');
//Serial.println(vel_l);
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
