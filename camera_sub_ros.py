import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32
import os,sys
import subprocess 


class RC_CAR_Subscriber(Node):
    def __init__(self):
      super().__init__('rc_car_subscriber')
      self.subscription1 = self.create_subscription(Int32,'rc_car1',self.listener_callback_msg1,10)
      self.subscription2 = self.create_subscription(String,'rc_car2',self.listener_callback_msg2,10)
      self.subscription1  # prevent unused variable warning
      self.subscription2  # prevent unused variable warning
      self.get_logger().info('rc car subscriber has been started.')

    def listener_callback_msg1(self, msg1):
        self.get_logger().info('I received x = %s' % msg1.data)
        if msg1.data>=400:
            print('turn right')
            cmd="gnome-terminal"
            PATH="python3 /home/jetson/servo_right.py"
            terminal_command="chmod +x servo_right.py"
            os.system(terminal_command)
            subprocess.Popen([cmd,'--','bash','-c',PATH])

        if msg1.data<=100:
            print('turn left')
            cmd="gnome-terminal"
            PATH="python3 /home/jetson/servo_left.py"
            terminal_command="chmod +x servo_left.py"
            os.system(terminal_command)
            subprocess.Popen([cmd,'--','bash','-c',PATH])
        

    def listener_callback_msg2(self, msg2):
        self.get_logger().info('I received depth = %s' % msg2.data)
        if msg2.data >=2:
            print('go!')
            cmd="gnome-terminal"
            terminal_command1="sudo chmod a+rw /dev/ttyUSB0"
            os.system(terminal_command1)
            PATH="python3 /home/jetson/DynamixelSDK/python/tests/protocol1_0/wheel_front.py"
            subprocess.Popen([cmd,'--','bash','-c',PATH])
        if msg2.data == 1:
            print("stop!")
            cmd="gnome-terminal"
            terminal_command1="sudo chmod a+rw /dev/ttyUSB0"
            os.system(terminal_command1)
            PATH="python3 /home/jetson/DynamixelSDK/python/tests/protocol1_0/wheel_stop.py"
            subprocess.Popen([cmd,'--','bash','-c',PATH])
        if msg2.data <=1:
            print("back!")
            cmd="gnome-terminal"
            terminal_command1="sudo chmod a+rw /dev/ttyUSB0"
            os.system(terminal_command1)
            PATH="python3 /home/jetson/DynamixelSDK/python/tests/protocol1_0/wheel_back.py"
            subprocess.Popen([cmd,'--','bash','-c',PATH])



def main(args=None):
   rclpy.init(args=args)
   rc_car_subscriber = RC_CAR_Subscriber()
   rclpy.spin(rc_car_subscriber)
   rc_car_subscriber.destroy_node()
   rclpy.shutdown()

if __name__=='__main__':
    main()
