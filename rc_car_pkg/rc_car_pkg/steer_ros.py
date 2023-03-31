import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32
import os,sys
import subprocess 
import Adafruit_PCA9685
import time

pwm = Adafruit_PCA9685.PCA9685(address = 0x40, busnum = 1)

servo_num = 6

servo_min    = 150 # min. pulse length
servo_max    = 600 # max. pulse length
servo_offset = 50

pwm.set_pwm_freq(60)
STATE2 = 1

def map(value,min_angle,max_angle,min_pulse,max_pulse):
    angle_range=max_angle-min_angle
    pulse_range=max_pulse-min_pulse
    scale_factor=float(angle_range)/float(pulse_range)
    return min_pulse+(value/scale_factor)

def set_angle(channel,angle):
    pulse=int(map(angle,0,180,servo_min,servo_max))
    pwm.set_pwm(channel,0,pulse)

class STEER_ROS(Node):
    def __init__(self):
        super().__init__('wheel_ros')
        self.subscription1 = self.create_subscription(String,'rc_car3',self.listener_callback_msg1,10)

        self.subscription1  # prevent unused variable warning
        self.get_logger().info('wheel ros subscriber has been started.')

    def listener_callback_msg1(self, msg1):
        global STATE2
        STATE2 = msg1.data
        self.get_logger().info('I received depth = %s' % msg1.data)
        
def main(args=None):
    rclpy.init(args=args)
    steer_ros = STEER_ROS()
    rclpy.spin(steer_ros)
    terminal_command1="sudo chmod a+rw /dev/ttyUSB0"
    os.system(terminal_command1)
    while rclpy.ok():

        if STATE2>=400:
            print('right!')
            while STATE2>=400:
                set_angle(5,90)
                set_angle(2,60)
                rclpy.spin_once(steer_ros)
                if STATE2 < 400:
                    break

        elif STATE2 <=100:
            print("left!")
            while STATE2 <=100:
                set_angle(5,0)
                set_angle(2,0)

                rclpy.spin_once(steer_ros)
                if STATE2 >100:
                    break 
           
        else:
            print("♩~♬~♪")
            while STATE2 >100 | STATE2< 400:
                set_angle(5,40)
                set_angle(2,0)
                rclpy.spin_once(steer_ros)  
                if STATE2 <=100 | STATE2>= 400:
                    break
        
    steer_ros.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()