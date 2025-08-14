from avarobotutils.drive import RobotDriveUtils
import time, math

def main():
    robot = RobotDriveUtils('swtest.ava8.net', 'username', 'password', 'SB00200', ip=None)

    driving = False
    docked = True

    # Runs program until robot docks
    while (robot.get_docked_status() != "Docked" or robot.get_state() == "Undocking"):
        stopped = False
        update = robot.get_updates()
        status = update["planStatus"] # Figures out new command to robot
        state = robot.get_state() # Current state of robot
        
        # Tries to get robot velocity
        try: 
            robot.get_velocity()
        except:
            stopped = True # Robot has stopped

        arriveAndScan(stopped, driving, status, robot) # Checks if robot has arrived to start scan routine
        
        # Checks if robot is moving to new tag
        if (status == "IN_PROGRESS" and "waypointGoal" in update and not driving):
            print("Robot driving to tag.")
            driving = True

        # Checks if robot is undocking
        if (state == "Undocking" and docked):
            print("Robot is undocking.")
            docked = False 

    print("Robot has docked.")

# Scans the space by creating a rectangle and then turn
def arriveAndScan(stopped, driving, status, robot: RobotDriveUtils):
    if (status == "COMPLETE" and stopped and driving):
        # Waits 10 seconds after robot has arrived to a tag
        print("Robot arrived at tag.")
        driving = False
        time.sleep(10)

        # Robot will perform a scan routine
        print("Performing scanning routine.")
        sidestep(robot, -2, 0.5) # robot moves to the right
        while (robot.get_zlift_pos() < 0.295): 
            robot.drive_zlift(1) # lift z-axis of robot
        robot.wait_on_complete()
        sidestep(robot, 4, 0.5) # robot moves to the left
        while (robot.get_zlift_pos() > 0.03):
            robot.drive_zlift(0) # lower z-axis of robot
        robot.wait_on_complete()
        sidestep(robot, -2, 0.5) # robot moves to the right
        print("Scanning routine completed.")

        time.sleep(5)

        print("Robot is turning.")
        turn(robot, math.pi * 2, 0.5) # robot turns 360 degrees
        print("Robot finished turning.")


# Sidestep function where distance to the left is positive and to the right is negative
def sidestep(robot: RobotDriveUtils, distance, speed):
    totalTime = abs(distance) / speed # total time to complete sidestep
    requestPeriod = 0.4
    done = False
    start_time = time.time()

    while not done:
        iterStart = time.time()
        duration = 0.5 # default duration for sidestepping
        # check if time left to complete sidestep is less than duration
        if iterStart > start_time + totalTime - duration:
            # final sidestep is less than 500 msec
            duration = start_time + totalTime - iterStart
            done = True
        robot.drive_robot(sidestep = distance, duration = duration)
        # delay the next request so that the duration between requests is requestPeriod
        req_time = time.time() - iterStart # time taken for this request
        if req_time < requestPeriod:
            time.sleep(requestPeriod - req_time)

# Rotation function which enables smooth rotation of robot
def turn(robot: RobotDriveUtils, radians, rotation):
    totalTime = radians / rotation # total time to complete desired rotation
    totalTime += 0.7
    requestPeriod = 0.4
    done = False
    startTime = time.time()

    while not done:
        iterStart = time.time()
        duration = 0.5 # default duration for turning
        # check if time left to complete turning is less than duration
        if iterStart > startTime + totalTime - duration:
            # final turn is less than 500 msec
            duration = startTime + totalTime - iterStart
            done = True
        robot.drive_robot(rotate = rotation, duration = duration)
        # delay next request so that duration between requests is requestPeriod
        reqTime = time.time() - iterStart # time taken for current request
        if reqTime < requestPeriod:
            time.sleep(requestPeriod - reqTime)

if __name__ == "__main__":
    main()