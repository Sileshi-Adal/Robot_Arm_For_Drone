def mapAngle(objectDistance):
    angle = 17*objectDistance - 75
    if angle < 0:
        angle *= -1
    servoValue = getElbowRotation(angle)
    print("mapAngle is done .... ", servoValue)
    return round(servoValue, 0)

def getBaseRotation(elbowAngle):
    servoValue = 3.75*elbowAngle + 150
    return round(servoValue, 0)
def startupBaseRotation(noRepetition):
    servoValue = 86*noRepetition + 170
    return round(servoValue, 0)
def getGripAngle(openningDegree):
    servoValue = 3.75 *  openningDegree + 150
    return round(servoValue, 0)
