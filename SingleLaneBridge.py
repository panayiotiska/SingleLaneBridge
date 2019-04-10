import threading
import time

mutex = threading.RLock()
turn = 0 # 0 for red, 1 for blue (initialized so red car starts first)
redCarsWaiting = 0 # number of red cars waiting to cross the bridge
blueCarsWaiting = 0 # number of blue cars waiting to cross the bridge

def crossBridge(count, color, crossTime):
    """thread bridge function"""
    global mutex
    global turn
    global redCarsWaiting
    global blueCarsWaiting
    trafficResult = checkTraffic()
    print (color, count, "arrived", end='\n', flush=True)

    if (trafficResult == 1):
        turn = 0
        color = 'red'
    elif (trafficResult == 2):
        turn = 1
        color = 'blue'

    mutex.acquire() #Critical Sections Start
    if ((turn == 0 and color == "red") or (turn == 1 and color == "blue")):
        print (color, count, " crossing...")
        time.sleep(crossTime)
        print (color, count, " crossed!")
        if (turn == 0): # changes the value of turn
            redCarsWaiting -= 1 # removes a red car from the waiting section
            turn = 1 # changes the turn to the other color-car
        else :
            blueCarsWaiting -= 1 # removes a blue car from the waiting section
            turn = 0 # changes the turn to the other color-car
        mutex.release() #Critical Section End
    else:
        mutex.release()

def checkTraffic(): # Decides whether there is traffic problem to the one side or the other
    """"traffic decission function"""
    global redCarsWaiting
    global blueCarsWaiting
    limit = 0.3 # limit allowed for more traffic in one side
    trafficPercentRed = 0 # indicates the significance of the problem for red cars (takes values from 0 to 1)
    trafficPercentBlue = 0 # indicates the significance of the problem for blue cars (takes values from 0 to 1)

    if (redCarsWaiting > blueCarsWaiting):
        trafficPercentRed = (redCarsWaiting - blueCarsWaiting) / (redCarsWaiting + blueCarsWaiting) # example: (7 red, 3 blue) => 4 / 10 = 0.4 > 0.3 => priority to red

    if (blueCarsWaiting > redCarsWaiting):
        trafficPercentBlue = (blueCarsWaiting - redCarsWaiting) / (blueCarsWaiting + redCarsWaiting)

    if (trafficPercentRed > limit):
        return 1 # Give priority to red

    elif (trafficPercentBlue > limit):
        return 2 # Give priority to blue

    else : return 0


if __name__ == '__main__':

    countRed = 0 # increasing for every new red car (car plate)
    countBlue = 0 # increasing for every new blue car (car plate)
    color = '' # color variable initialization

    #numOfThreads = input("Num of threads? ")
    #arriveTime = input("Arrive every? ")
    #crossTime = input("Cross time? ")

    numOfThreads = 20 # number of maximum threads/cars that will arrive
    arriveTime = 5 # time needed for a thread/car to arrive
    crossTime = 10 # time needed for a thread/car to cross the bridge

    for i in range (numOfThreads) :
        time.sleep(arriveTime)
        for j in range (3): #to cause the problem
            r = threading.Thread(target=crossBridge, args=(countRed,'red',crossTime,))
            r.start()
            countRed += 1
            redCarsWaiting += 1
        b = threading.Thread(target=crossBridge, args=(countBlue,'blue',crossTime,))
        b.start()
        countBlue += 1
        blueCarsWaiting += 1
