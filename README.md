
# Team Member
Sileshi Adal (TL), Dagmawi Mallie, Han Jinkun, Zhao Chongyang, Wang Wengang, Wang Jun

http://capstone.utu.fi/en-RobotArm

# Goal
The ultimate goal of this project was to build an autonomous robot arm attached to the drone in order to grasp and drop objects to the desired place.

# Implementation
The robot arm is built on two raspberry Pi “Model B” single-board computers, one is for computing the functionality of the arm and the other is for computing video and image processing purposes. The arm attached on a FlameWheel 450 drone and controlled or ordered through a web based communication module to our server with the support of raspberry-pi camera for image processing and two ultrasonic sensors, which is used for measuring the distance of the object and for notifying the arm while the drone is either on flying or landing mode, in order to grasp and drop the objects to the desired place.

# Future development
Design more intelligent features to the current achieved result, for instance the arm should have more than two gripers for convenient methods of grasping and holding the object, increasing the degree of freedom for the translational movements of the arm, add a pressure sensor on the griper, which is fed into to the arm algorithm so that it can recognize while grasping the object. Additionally, instead of raspberry pi camera it will be more convenient and better to use Lidar sensing technology, and needs to implement a Communication module between the drone and arm to be fully realize actual autonomous behavior.

# Instruction how to run the codes   
- Open the xampp control panel to run the server.
- create the database on php myadmin page
- Give access to the ip address of both raspberries
- open the php script and run the browser as the local host
- run python scripts on each raspberries
- make sure you wrote the correct values on python scripts 
