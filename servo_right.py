#chmod +x servo_right.py
#python3 servo_right.py

import Adafruit_PCA9685
import time

pwm = Adafruit_PCA9685.PCA9685(address = 0x40, busnum = 1)

# Number of servo
servo_num = 6

servo_min    = 150 # min. pulse length
servo_max    = 600 # max. pulse length
servo_offset = 50

pwm.set_pwm_freq(60)

def map(value,min_angle,max_angle,min_pulse,max_pulse):
    angle_range=max_angle-min_angle
    pulse_range=max_pulse-min_pulse
    scale_factor=float(angle_range)/float(pulse_range)
    return min_pulse+(value/scale_factor)

def set_angle(channel,angle):
    pulse=int(map(angle,0,180,servo_min,servo_max))
    pwm.set_pwm(channel,0,pulse)



while True:
    print('degree:90')
    set_angle(5,0)
    set_angle(2,0)
    time.sleep(5)

    print('degree: 0')
    set_angle(5,120)
    set_angle(2,120)
    time.sleep(5)


