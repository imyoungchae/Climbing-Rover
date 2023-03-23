import rclpy
import os,sys
import subprocess 

from rclpy.node import Node
from std_msgs.msg import String

class RCSubscriber(Node):

    def __init__(self):
        super().__init__('rc_car_subscriber')
        self.subscription_ = self.create_subscription(String, 'keyboard_input_topic', self.keyboard_input_callback, 10)
        self.subscription_

    def keyboard_input_callback(self, msg):
        command = msg.data

        if command == 'forward':
            self.move_forward()
        elif command == 'left':
            self.turn_left()
        elif command == 'right':
            self.turn_right()
        elif command == 'stop':
            self.stop_car()
        elif command == 'exit':
            self.shutdown_node()

    def move_forward(self):
        print('go!')
        cmd="gnome-terminal"
        terminal_command1="sudo chmod a+rw /dev/ttyUSB0"
        os.system(terminal_command1)
        PATH="python3 /home/jetson/DynamixelSDK/python/tests/protocol1_0/wheel_front.py"
        subprocess.Popen([cmd,'--','bash','-c',PATH])


    def turn_left(self):
        print('turn left')
        cmd="gnome-terminal"
        PATH="python3 /home/jetson/servo_left.py"
        terminal_command="chmod +x servo_left.py"
        os.system(terminal_command)
        subprocess.Popen([cmd,'--','bash','-c',PATH])
        
    def turn_right(self):
        print('turn right')
        cmd="gnome-terminal"
        PATH="python3 /home/jetson/servo_right.py"
        terminal_command="chmod +x servo_right.py"
        os.system(terminal_command)
        subprocess.Popen([cmd,'--','bash','-c',PATH])

    def stop_car(self):
        print('back')
        cmd="gnome-terminal"
        terminal_command1="sudo chmod a+rw /dev/ttyUSB0"
        os.system(terminal_command1)
        PATH="python3 /home/jetson/DynamixelSDK/python/tests/protocol1_0/wheel_back.py"
        subprocess.Popen([cmd,'--','bash','-c',PATH])

    def shutdown_node(self):
        print('stop')
        cmd="gnome-terminal"
        terminal_command1="sudo chmod a+rw /dev/ttyUSB0"
        os.system(terminal_command1)
        PATH="python3 /home/jetson/DynamixelSDK/python/tests/protocol1_0/wheel_stop.py"
        subprocess.Popen([cmd,'--','bash','-c',PATH])

def main(args=None):
    print("let's go!")
    rclpy.init(args=args)
    rc_subscriber = RCSubscriber()
    rclpy.spin(rc_subscriber)
    rc_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
