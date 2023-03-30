import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np
from std_msgs.msg import String, Int32
import matplotlib.pyplot as plt
import pyrealsense2 as rs
from rclpy.qos import QoSProfile

pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 320, 240, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
profile = pipe.start(config)

frameset = pipe.wait_for_frames()
color_frame = frameset.get_color_frame()
color_init = np.asanyarray(color_frame.get_data())

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

class RC_CAR(Node):
    def __init__(self):
      super().__init__('rc_car')
      qos_profile = QoSProfile(depth=10)
      self.publisher1_ = self.create_publisher(Int32, 'rc_car1', qos_profile)
      self.publisher2_ = self.create_publisher(String, 'rc_car2', qos_profile)
      self.timer_=self.create_timer(0.1,self.rc_car_callback)
      self.get_logger().info('rc car publisher has been started.')

    def rc_car_callback(self):
        try:
         while True:
            frameset = pipe.wait_for_frames()
            color_frame = frameset.get_color_frame()
            depth_frame = frameset.get_depth_frame()

            color = np.asanyarray(color_frame.get_data())
            res = color.copy()
            hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)

            l_b = np.array([24, 133, 48])
            u_b = np.array([39, 200, 181])

            mask = cv2.inRange(hsv, l_b, u_b)
            color = cv2.bitwise_and(color, color, mask=mask)

            colorizer = rs.colorizer()
            colorized_depth = np.asanyarray(colorizer.colorize(depth_frame).get_data())

            align = rs.align(rs.stream.color)
            frameset = align.process(frameset)

            aligned_depth_frame = frameset.get_depth_frame()
            colorized_depth = np.asanyarray(colorizer.colorize(aligned_depth_frame).get_data())

            global color_init
            d = cv2.absdiff(color_init, color)
            gray = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, th = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(th, np.ones((3, 3), np.uint8), iterations=3)
            (c, _) = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(color, c, -1, (0, 255, 0), 2)
            color_init = color

            depth = np.asanyarray(aligned_depth_frame.get_data())

            for contour in c:
                if cv2.contourArea(contour) < 1500:
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                bottomLeftCornerOfText = (x, y)

                # Crop depth data:
                depth = depth[x:x+w, y:y+h].astype(float)

                depth_crop = depth.copy()

                if depth_crop.size == 0:
                    continue
                depth_res = depth_crop[depth_crop != 0]


                # Get data scale from the device and convert to meters
                depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
                depth_res = depth_res * depth_scale

                if depth_res.size == 0:
                    continue

                dist = min(depth_res)

                cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 3)
                text = "Depth: " + str("{0:.2f}").format(dist)
                dp=str("{0:.0f}").format(dist)

                msg1=Int32()
                msg1.data=x

                msg2=String()
                msg2.data=dp

                self.get_logger().info('x={}, depth={}'.format(x,dp))

                self.publisher1_.publish(msg1)
                self.publisher2_.publish(msg2)

                cv2.putText(res,
                            text,
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            lineType)

            cv2.namedWindow('RBG', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RBG', res)
            cv2.waitKey(1)            
        finally:
            pipe.stop()

def main(args=None):
   rclpy.init(args=args)
   rc_car=RC_CAR()
   rclpy.spin(rc_car)
   rc_car.destroy_node()
   rclpy.shutdown()

if __name__=='__main__':
    main()

