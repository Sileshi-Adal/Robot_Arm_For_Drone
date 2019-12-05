import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Disable warnings

#set right GPIO Pins
TRIGGER1 = 23
ECHO1 = 24

TRIGGER2 = 17
ECHO2 = 27

GPIO.setup(TRIGGER1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)

GPIO.setup(TRIGGER2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

def getReading1():
    # set Trigger to HIGH
    GPIO.output(TRIGGER1, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER1, False)

    StartTime = time.time()
    StopTime = time.time()

    retries = 0
    # save StartTime
    while GPIO.input(ECHO1) == 0:
        retries = retries + 1
        if retries > 5000:
            return 540
        StartTime = time.time()

    # save time of arrival
    retries = 0
    while GPIO.input(ECHO1) == 1:
        retries = retries + 1
        #print("right", retries)
        if retries > 5000:
            return 541
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s = 343 000 mm/s)
    #distance = (TimeElapsed * 343000) / 2
    distance = TimeElapsed *17150
    distance = round(distance, 2)
    return distance

def getReading2():
    # set Trigger to HIGH
    GPIO.output(TRIGGER2, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER2, False)

    StartTime = time.time()
    StopTime = time.time()

    retries = 0
    # save StartTime
    while GPIO.input(ECHO2) == 0:
        retries = retries + 1
        if retries > 5000:
            return 540
        StartTime = time.time()

    # save time of arrival
    retries = 0
    while GPIO.input(ECHO2) == 1:
        retries = retries + 1
        #print("right", retries)
        if retries > 5000:
            return 541
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s = 343 000 mm/s)
    #distance = (TimeElapsed * 343000) / 2
    distance = TimeElapsed *17150
    distance = round(distance, 2)
    return distance
