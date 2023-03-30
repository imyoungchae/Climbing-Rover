import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32

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

    def listener_callback_msg2(self, msg2):
        self.get_logger().info('I received depth = %s' % msg2.data)


def main(args=None):
   rclpy.init(args=args)
   rc_car_subscriber = RC_CAR_Subscriber()
   rclpy.spin(rc_car_subscriber)
   rc_car_subscriber.destroy_node()
   rclpy.shutdown()

if __name__=='__main__':
    main()