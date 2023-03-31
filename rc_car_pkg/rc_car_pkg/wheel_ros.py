import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32
import os,sys
import subprocess 

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_MX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL0_ID                      = 0  
DXL1_ID                      = 1  
DXL2_ID                      = 2  
DXL3_ID                      = 3  
DXL4_ID                      = 4  
DXL5_ID                      = 5  

BAUDRATE                    = 1000000            # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold
MOVING_SPEED=32
index = 0


portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL0_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel0 has been successfully connected")

# Enable Dynamixel1 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel1 has been successfully connected")

# Enable Dynamixel2 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel2 has been successfully connected")

# Enable Dynamixel3 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL3_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel3 has been successfully connected")

# Enable Dynamixel4 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL4_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel4 has been successfully connected")

# Enable Dynamixel5 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL5_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel5 has been successfully connected")



STATE = 1


class WHEEL_ROS(Node):
    def __init__(self):
        super().__init__('wheel_ros')
        self.subscription2 = self.create_subscription(String,'rc_car4',self.listener_callback_msg2,10)

        self.subscription2  # prevent unused variable warning
        self.get_logger().info('wheel ros subscriber has been started.')

    def listener_callback_msg2(self, msg2):
        global STATE
        STATE = int(msg2.data)
        self.get_logger().info('I received depth = %s' % msg2.data)
        

    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0


def main(args=None):
    rclpy.init(args=args)
    wheel_ros = WHEEL_ROS()

    terminal_command1="sudo chmod a+rw /dev/ttyUSB0"
    os.system(terminal_command1)

    while rclpy.ok():
        if int(STATE)>=2:
            print('go!')
            while int(STATE)>=3:
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL0_ID, MOVING_SPEED,1424)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL1_ID, MOVING_SPEED,1424)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL2_ID, MOVING_SPEED,1424)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL3_ID, MOVING_SPEED,400)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL4_ID, MOVING_SPEED,400)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL5_ID, MOVING_SPEED,400) 
                rclpy.spin_once(wheel_ros)
                if int(STATE) < 3:
                    break
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL0_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)

        if int(STATE)>=2:
            print('go!')
            while int(STATE)>=2:
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL0_ID, MOVING_SPEED,1204)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL1_ID, MOVING_SPEED,1204)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL2_ID, MOVING_SPEED,1204)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL3_ID, MOVING_SPEED,200)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL4_ID, MOVING_SPEED,200)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL5_ID, MOVING_SPEED,200) 
                rclpy.spin_once(wheel_ros)
                if int(STATE) < 1:
                    break
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL0_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)


        elif int(STATE) == 1:
            print("stop!")
            while int(STATE)== 1:
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL0_ID, MOVING_SPEED,0)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL1_ID, MOVING_SPEED,0)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL2_ID, MOVING_SPEED,0)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL3_ID, MOVING_SPEED,0)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL4_ID, MOVING_SPEED,0)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL5_ID, MOVING_SPEED,0)
                rclpy.spin_once(wheel_ros)
                if int(STATE) != 1:
                    break 
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL0_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)


 
            
        elif int(STATE) <=1:
            print("back!")
            while int(STATE) <=1:
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL0_ID, MOVING_SPEED,200)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL1_ID, MOVING_SPEED,200)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL2_ID, MOVING_SPEED,200)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL3_ID, MOVING_SPEED,1204)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL4_ID, MOVING_SPEED,1204)  
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL5_ID, MOVING_SPEED,1204)
                rclpy.spin_once(wheel_ros)  
                if int(STATE) >1:
                    break
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL0_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)


        
    wheel_ros.destroy_node()
    rclpy.shutdown()
    portHandler.closePort()

if __name__=='__main__':
    main()