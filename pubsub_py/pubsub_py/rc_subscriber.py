import rclpy
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
        # execute code to move RC car forward
        print('hi')

    def turn_left(self):
        # execute code to turn RC car left
        print('hi')

    def turn_right(self):
        print('hi')
        # execute code to turn RC car right

    def stop_car(self):
        print('hi')
        # execute code to stop RC car

    def shutdown_node(self):
        self.get_logger().info('RC car subscriber has been stopped.')
        self.destroy_node()
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    rc_subscriber = RCSubscriber()
    rclpy.spin(rc_subscriber)
    rc_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()