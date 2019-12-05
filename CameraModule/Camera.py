import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

import mysql.connector
from mysql.connector import connection, errorcode, Error
import sys, gc
config = {
        'user':'eagles',
        'password': 'UniversityOfTurku',
        'host': '192.168.43.11',
        'database':'roboticarm',
}

class VideoFeedback():
    """docstring for VideoFeedback."""
    def __init__(self, threshold):
        super(VideoFeedback, self).__init__()
        self.thresholdValue = threshold
        self.camera = PiCamera()
        self.f_width = 640
        self.f_height = 480
        self.camera.resolution = (self.f_width, self.f_height)
        self.camera.framerate = 32
        resolution = (self.f_width, self.f_height)
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port = True)
        self.image = None

        time.sleep(0.1)

        self.windowLength = 70 # number of frames
        self.window = [self.windowLength] #holds the value of similarity index for each frame

        for i in range(self.windowLength):
            self.window.append(0)
#coordinate for green square box, we trim out this box for similarity ananlysis
        self.x_top_left = int(self.f_width/3)
        self.y_top_left = int((self.f_height/2) + (self.f_height/4))
        self.x_bottom_right = int((self.f_width/3)*2)
        self.y_bottom_right = int((self.f_height/2) - (self.f_height/4))
        self.stored_image = None
        self.noFrame = 0
        self.average = 0
#X1, X2,..,X4 is the value of each digit in the statusreport table
        self.X2 = 1
        self.X3 = 1
        self.X4 = 1
        self.X1 = 2
        self.conn = None
        self.cursor = None
        self.isOperationDone = False
        self.keypoints_2 = None
        self.descriptor_2 = None
        self.orb_detector = None
        self.startTime = None
    def connect(self):
        try:
            self.conn = mysql.connector.connect(**config)
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
        except Error as e:
            print(e)
    def close(self):
        self.conn.close()
        self.cursor.close()
#returns in integer based on the degree of similarity if the value is b/n 170 t0 250 ,then with high degree certainity the picture in the frame is same as the one in memory
    def ObjectDetector(self, input_image):
        gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        (keypoints_1, descriptor_1) = self.orb_detector.detectAndCompute(gray, None)
        brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches_found =  brute_force.match(descriptor_1,self.descriptor_2)
        matches_found = sorted(matches_found, key=lambda val: val.distance)

        return len(matches_found)
#calculate the mean of the values calculated by the algorithm.
    def movingAverage(self, similarityIndex):
        if self.X2 == 1:# continue with vision analysis
            for i in range(self.windowLength-1): #attach value of similarity index on fifo array
                self.window[i] = self.window[i+1]
            self.window[self.windowLength-1] = similarityIndex
            self.noFrame += 1
            self.average = np.mean(self.window)
            self.average = round(self.average, 0)

            if self.noFrame == self.windowLength: # when array is full
                print("self.window: ", self.window)
                self.noFrame = 0
                self.ObjectFinder() #make decision
            self.startTime = time.time() # reset the count
        else: # rotate the camera
            stopTime = time.time()
            self.fetchStatusReport()
            timeElapsed = round((stopTime - self.startTime), 0)
#if there is no response from other raspberry for 30 sec discontinue operation
            if timeElapsed > 30: # reset the status value
                self.X1 = 1
                self.X2 = 1
                self.X3 = 1
                self.X4 = 1
                print("timeElapsed: ", timeElapsed)
                self.UpdateTable_statusreport() # report that the operation is Failed
                self.UpdateTable_task() #update the value
                self.isOperationDone = True
    def UpdateTable_task(self):
        self.connect()
        queryID = '''SELECT taskId FROM statusreport WHERE id = %s '''
        rowNo = 1
        self.cursor.execute(queryID,(rowNo, ))
        queryReturn = self.cursor.fetchone()
        taskId = queryReturn[0]
        query = ''' UPDATE task SET status = %s WHERE id = %s'''
        status = "Mission Failed"
        self.cursor.execute(query,(status, taskId))
        self.conn.commit()
        self.close()

    def ObjectFinder(self):
        self.average = np.mean(self.window)
        self.average = round(self.average,0)
        if (self.average >= self.thresholdValue) and (self.average <= (self.thresholdValue + 80)): #if object is detected
            self.X3 = 2 #the other raspberry will know that object is found
            self.X1 = 1
            self.X2 = 1
            self.isOperationDone = True #kill the camera object
        else:
            if self.X4 == 2:
                self.isOperationDone = True
            else:
                self.X2 = 2
        self.UpdateTable_statusreport() #updat the database with the value
    def UpdateTable_statusreport(self):
        self.connect()
        query = ''' UPDATE statusreport SET  cameraStatus = %s WHERE id = %s '''
        rowNo = 1
        updateValue = self.X4*1000 + self.X3*100 + self.X2*10 + self.X1
        print("X4: ", self.X4, " X3: ", self.X3, " X2: ", self.X2, " X1: ", self.X1)
        self.cursor.execute(query, (updateValue, rowNo,))
        self.conn.commit()
        self.close()
    def fetchStatusReport(self):
        self.connect()
        query = ''' SELECT cameraStatus FROM statusreport WHERE id = %s '''
        tableRow = 1
        self.cursor.execute(query, (tableRow,))
        queryReturn = self.cursor.fetchone()
        cameraStatus = int(queryReturn[0])
        print("cameraStatus: ", cameraStatus)
        self.X1 = int(cameraStatus % 10)
        self.X2 = int((cameraStatus % 100)/10)
        self.X3 = int((cameraStatus % 1000)/ 100)
        self.X4 = int(cameraStatus / 1000)
        self.close()
    def closeOperation(self): #closing the camera object
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
        cv2.destroyAllWindows()
    def __del__(self):
        pass
    def Recording(self,picture): #Recording object
        print(picture)
        collected = gc.collect() # clean the garbage at the start of operation
        self.stored_image = cv2.imread(picture, 0) # read the Picture
        self.orb_detector = cv2.ORB_create(1300, 1.3)
        (self.keypoints_2, self.descriptor_2) = self.orb_detector.detectAndCompute(self.stored_image, None) # calucualte the descriptor and keypoints for the image we uploaded
        self.startTime = time.time() #mark the time the operation starts
        for frame in self.stream: #for each frame recorded
            image2 = frame.array
            self.image = cv2.flip(image2,0) #flip it upside down according to the direction of camera we situated
            cv2.rectangle(self.image,(self.x_top_left, self.y_top_left),(self.x_bottom_right, self.y_bottom_right),(255,0,0),4)
            cropped_image = self.image[self.y_bottom_right:self.y_top_left,self.x_top_left:self.x_bottom_right]
            cropped_image = cv2.flip(cropped_image,1) # crop out the image inside the rectangle
            similarity = self.ObjectDetector(cropped_image) # calculate similarity in ORB algorithm
            self.movingAverage(similarity) # calculate the mean value
            message = "match points: " + str(self.average)

            cv2.putText(self.image, message, (150,400), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255,51),4)
            cv2.imshow("frame", self.image)

            self.rawCapture.truncate(0)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"): # pressing q on keyboard will close the operation
                self.closeOperation()
                break

            if self.isOperationDone:
                self.closeOperation()
                break
