#include<Encoder.h>
#include <ros.h>
#include <ros/time.h>
#include <geometry_msgs/PointStamped.h>
#include <geometry_msgs/Twist.h>

Encoder enc_R(2, 3); //encoder input
Encoder enc_L(18, 19);
int Left_motor_pwm = 9;
int Right_motor_pwm = 8;
int Left_dir = 23;  // HIGH is forward
int Right_dir = 22;

ros::NodeHandle  nh;
geometry_msgs::PointStamped msg;

void messageCb( const geometry_msgs::Twist& vel){
  if(vel.linear.x == 0.5 && vel.angular.z ==0)
  {
    digitalWrite(Right_dir, HIGH);
    digitalWrite(Left_dir, HIGH);
    analogWrite(Right_motor_pwm, 100);
    analogWrite(Left_motor_pwm, 100);
  }
  else if(vel.linear.x == 0 && vel.angular.z == 1)
  {
    digitalWrite(Right_dir, HIGH);
    digitalWrite(Left_dir, LOW);
    analogWrite(Right_motor_pwm, 25);
    analogWrite(Left_motor_pwm, 25);
  }
  else if(vel.linear.x == 0 && vel.angular.z == -1)
  {
    digitalWrite(Right_dir, LOW);
    digitalWrite(Left_dir, HIGH);
    analogWrite(Right_motor_pwm, 25);
    analogWrite(Left_motor_pwm, 25);
  }
  else if(vel.linear.x == -0.5 && vel.angular.z == 0)
  {
    digitalWrite(Right_dir, HIGH);
    digitalWrite(Left_dir, LOW);
    analogWrite(Right_motor_pwm, 100);
    analogWrite(Left_motor_pwm, 100);
  }
  else
  {
    analogWrite(Right_motor_pwm, 0);
    analogWrite(Left_motor_pwm, 0);
  }
}

ros::Subscriber<geometry_msgs::Twist> sub("/cmd_vel", messageCb);
ros::Publisher encoder("encoder", &msg);

void setup() {

  nh.initNode();
  nh.advertise(encoder);
  nh.subscribe(sub);

  Serial.begin(115200);
  Serial.println("Basic Encoder Test:");

  //Motor Left
  pinMode(9, OUTPUT); //PWM_L
  pinMode(18, INPUT); //EncoderLB
  pinMode(19, INPUT); //EncoderLA
  pinMode(23, OUTPUT); //DIR_L

  //Motor Right
  pinMode(22, OUTPUT); //DIR_R
  pinMode(8, OUTPUT); //PWM_R
  pinMode(2, INPUT);  //EN_RA
  pinMode(3, INPUT);  //EN_RB

  //Set Test PWM
  analogWrite(Right_motor_pwm, 0);
  analogWrite(Left_motor_pwm, 0);
}

double cur_enc_L = 0, cur_enc_R = 0;
void loop() {
  
  cur_enc_L = enc_L.read();
  cur_enc_R = enc_R.read();

  msg.header.stamp = nh.now();
  msg.header.frame_id = "world";
  msg.point.x = cur_enc_L;
  msg.point.y = cur_enc_R;

  encoder.publish(&msg);
  nh.spinOnce();
  delay(5);

  //  Serial.println(newpos);

}
