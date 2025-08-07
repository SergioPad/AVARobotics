from avarobotutils.drive import RobotDriveUtils
import time

def main():
    robot = RobotDriveUtils('swtest.ava8.net', 'username', 'password', 'SB00200', ip=None)

    driving = False
    docked = True

    # Runs program until robot docks
    while (robot.get_docked_status() != "Docked" or robot.get_state() == "Undocking"):
        # Obtains robot state and update as it moves
        stopped = False
        update = robot.get_updates()
        status = update["planStatus"]
        state = robot.get_state()
        
        # Checks if robot is stopped
        try: 
            robot.get_velocity()
        except:
            stopped = True

        # Checks if robot has arrived to tag and spins
        arriveAndSpin(stopped, driving, status, robot)
        
        # Checks if robot is moving to new tag
        if (status == "IN_PROGRESS" and "waypointGoal" in update and not driving):
            print("Robot driving to tag.")
            driving = True

        # Checks if robot is undocking
        if (state == "Undocking" and docked):
            print("Robot is undocking.")
            docked = False 

    print("Robot has docked.")

# Checks if robot has arrived at a tag and stopped
def arriveAndSpin(stopped, driving, status, robot: RobotDriveUtils):
    if (status == "COMPLETE" and stopped and driving):
        # Waits 10 seconds after robot has arrived
        print("Robot arrived at tag.")
        driving = False
        time.sleep(10)

        # Spins the robot 360 degrees
        print("Robot will begin to spin.")
        for _ in range(24):
            robot.drive_robot(0.0, 1, 0.0, 0.5)
        print("Robot finished spinning.")
     

if __name__ == "__main__":
    main()