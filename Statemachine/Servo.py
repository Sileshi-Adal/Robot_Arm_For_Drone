from __future__ import division
import time
import Adafruit_PCA9685
#initialise the PCA9685
pwm = Adafruit_PCA9685.PCA9685()

pwm.set_pwm_freq(60)

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000
    pulse_length //= 60
    pulse_length //= 4096
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, int(pulse))
def gripperServo(channel, pulse):
    set_servo_pulse(channel,pulse)
def baseServo(channel, pulse):
    #set_servo_pulse(channel,pulse)
    pwm.set_pwm(channel, 0, pulse)
def heightServo(channel, pulse):
    pwm.set_pwm(channel, 0, pulse)
