import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class KeyboardInputPublisher(Node):

    def __init__(self):
        super().__init__('keyboard_input_publisher')
        self.publisher_ = self.create_publisher(String, 'keyboard_input_topic', 10)

        self.timer_ = self.create_timer(0.1, self.keyboard_input_callback)
        self.get_logger().info('Keyboard input publisher has been started.')

    def keyboard_input_callback(self):
        keyboard_input = input('Enter a command (w(go), a(right), s(back), d(left), x(stop): ')

        if keyboard_input == 'w':
            command = 'forward'
        elif keyboard_input == 'a':
            command = 'left'
        elif keyboard_input == 'd':
            command = 'right'
        elif keyboard_input == 's':
            command = 'stop'
        elif keyboard_input == 'x':
            command = 'exit'
        else:
            command = ''

        if command:
            msg = String()
            msg.data = command
            self.publisher_.publish(msg)

            if command == 'exit':
                self.get_logger().info('stop!!!!!!!!!!!!!!!!!!')



def main(args=None):
    rclpy.init(args=args)
    keyboard_input_publisher = KeyboardInputPublisher()
    rclpy.spin(keyboard_input_publisher)
    keyboard_input_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
