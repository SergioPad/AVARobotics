from avarobotutils.drive import RobotDriveUtils
import random

def main():
    robot = RobotDriveUtils('swtest.ava8.net', 'username', 'password', 'SB00200', ip=None)
    
    try:
        if robot.get_docked_info()["state"] == "Docked":
            # Get tag list
            tags = findPossibleTags(robot)

            # Undock robot
            print("Robot is docked. Undocking...")
            robotUndocked = robot.undock_robot_using_drive()

            if robotUndocked:
                # Drive to two tags and rotate 360 degrees
                for _ in range(2):
                    driveTag = tags[random.randint(0, len(tags) - 1)]
                    tags.remove(driveTag)

                    print(f"Driving to tag: {driveTag}")
                    robot.drive_robot_to_tag(driveTag, "1")
                    robot.wait_on_complete()

                    print("Reached tag. Now rotating...")
                    for _ in range(24):
                        robot.drive_robot(0.0, 1, 0.0, 0.5)

                # Dock robot
                print("Docking...")
                robotDocked = robot.dock_home()
                if robotDocked:
                    print("Docked successfully")
        else:
            print("Robot is not docked. Dock first :)")
            robot.dock_home()

    except Exception as e:
        print(f"Error found: {e}")


def findPossibleTags(robot: RobotDriveUtils):
    # Finds tags that aren't docks
    tags = robot.get_tag_list("1")
    tagNum = list()

    for i in list(tags.keys()):
        if "Dock" not in tags[i]["name"] and "Dock" not in tags[i]["attributes"]["TagType"]:
            tagNum.append(i)

    # Returns drivable tags
    return tagNum

if __name__ == "__main__":
    main()