import threading
import time

import airsim
import keyboard
import numpy as np


class ServerThread(threading.Thread):
    """
    The thread executes commands to the Airsim client. As a default, the run method enables keyboard control over the drone.
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.logger = None
        self.cameraAngleDeg = 0

        # Initialize Airsim client
        self.client = airsim.MultirotorClient()  # connect to the simulator
        self.client.confirmConnection()
        self.client.reset()
        self.client.enableApiControl(True)  # enable API control on Drone
        self.client.armDisarm(True)  # arm Drone
        time.sleep(0.5)
        
    def takeoff(self):
        self.client.takeoffAsync().join()  # let drone take-off

    def stop(self):
        """
        Method to be called when the thread should be stopped
        :return:
        """
        print("Thread stop")
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        """
        Method to be executed by the thread.
        The actions performed by the drone should be used here
        :return:
        """
        keyboard.add_hotkey('w', self.forward, timeout=0)
        keyboard.add_hotkey('s', self.back, timeout=0)
        keyboard.add_hotkey('a', self.left, timeout=0)
        keyboard.add_hotkey('d', self.right, timeout=0)
        keyboard.add_hotkey('e', self.turnRight, timeout=0)
        keyboard.add_hotkey('q', self.turnLeft, timeout=0)
        keyboard.add_hotkey('page up', self.up, timeout=0)
        keyboard.add_hotkey('page down', self.down, timeout=0)
        keyboard.add_hotkey('space', self.hover, timeout=0)
        keyboard.add_hotkey('t', self.takeoff, timeout=0)
        # goto interface exists, too

        keyboard.wait('esc')  # wait until 'esc' pressed, upon which the thread finishes

    #########################################
    # Possible actions on the drone
    #########################################

    def forward(self, speedMultiplier: float = 5):
        """
        Method implements forward movement of the drone (via connection to Airsim client)
        :param speedMultiplier:
        :return:
        """
        try:
            self.logger.info("Command received: Move Forward")
            xSpeed = np.cos(np.deg2rad(self.cameraAngleDeg)) * speedMultiplier
            ySpeed = np.sin(np.deg2rad(self.cameraAngleDeg)) * speedMultiplier
            zSpeed = 0  # Vertical
            self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                            airsim.YawMode(False, self.cameraAngleDeg))
        except:
            pass

    def back(self, speedMultiplier: float = 5):
        """
        Method implements backward movement of the drone (via connection to Airsim client)
        :param speedMultiplier:
        :return:
        """
        try:
            self.logger.info("Command received: Move Back")
            xSpeed = -np.cos(np.deg2rad(self.cameraAngleDeg)) * speedMultiplier
            ySpeed = -np.sin(np.deg2rad(self.cameraAngleDeg)) * speedMultiplier
            zSpeed = 0  # Vertical
            self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                            airsim.YawMode(False, self.cameraAngleDeg))
        except:
            pass

    def left(self, speedMultiplier: float = 5):
        """
        Method implements left-side movement of the drone (via connection to Airsim client)
        :param speedMultiplier:
        :return:
        """
        try:
            self.logger.info("Command received: Move Left")
            xSpeed = -np.sin(np.deg2rad(self.cameraAngleDeg)) * speedMultiplier
            ySpeed = -np.cos(np.deg2rad(self.cameraAngleDeg)) * speedMultiplier
            zSpeed = 0  # Vertical
            self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                            airsim.YawMode(False, self.cameraAngleDeg))
        except:
            pass

    def right(self, speedMultiplier: float = 5):
        """
        Method implements right-side movement of the drone (via connection to Airsim client)
        :param speedMultiplier:
        :return:
        """
        try:
            self.logger.info("Command received: Move Right")
            xSpeed = np.sin(np.deg2rad(self.cameraAngleDeg)) * speedMultiplier
            ySpeed = np.cos(np.deg2rad(self.cameraAngleDeg)) * speedMultiplier
            zSpeed = 0  # Vertical
            self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                            airsim.YawMode(False, self.cameraAngleDeg))
        except:
            pass

    def turnRight(self, degreesToTurn: float = 5):
        """
        Method implements clockwise turning of the drone (via connection to Airsim client)
        :param degreesToTurn:
        :return:
        """
        try:
            self.logger.info("Command received: Turn right by 5 degrees")
            self.cameraAngleDeg += degreesToTurn
            xSpeed = 0
            ySpeed = 0
            zSpeed = 0  # Vertical
            self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                            airsim.YawMode(False, self.cameraAngleDeg))
        except:
            pass

    def turnLeft(self, degreesToTurn: float = 5):
        """
        Method implements anti-clockwise turning of the drone (via connection to Airsim client)
        :param degreesToTurn:
        :return:
        """
        try:
            self.logger.info("Command received: Turn left by 5 degrees")
            self.cameraAngleDeg -= degreesToTurn
            xSpeed = 0
            ySpeed = 0
            zSpeed = 0  # Vertical
            self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                            airsim.YawMode(False, self.cameraAngleDeg))
        except:
            pass

    def up(self, verticalSpeed: float = 2):
        """
        Method implements upward movement of the drone (via connection to Airsim client)
        :param verticalSpeed:
        :return:
        """
        try:
            self.logger.info("Command received: Move Up")
            xSpeed = 0
            ySpeed = 0
            zSpeed = -verticalSpeed  # Vertical
            self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 0.5, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                            airsim.YawMode(False, self.cameraAngleDeg))
        except:
            pass

    def down(self, verticalSpeed: float = 2):
        """
        Method implements downward movement of the drone (via connection to Airsim client)
        :param verticalSpeed:
        :return:
        """
        try:
            self.logger.info("Command received: Move Down")
            xSpeed = 0
            ySpeed = 0
            zSpeed = verticalSpeed  # Vertical
            self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 0.5, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                            airsim.YawMode(False, self.cameraAngleDeg))
        except:
            pass

    def hover(self):
        """
        Let the drone hover
        :return:
        """
        self.logger.info("Command received: Hover")
        self.client.hoverAsync()

    def goto(self, x, y, z, velocity, hasToFinish=False):
        """
        implementing goto: given a set of coordinates (x, y, z) and velocity with which to get to said coordinates (in Airsim coordinate system)
        :param x: x coordinate of destination point
        :param y: y coordinate of destination point
        :param z: z coordinate of destination point
        :param velocity: desired velocity
        :param hasToFinish: Whether the action should be stoppable while running
        :return:
        """
        self.logger.info("Command received: goto")
        if hasToFinish:  # yes
            self.client.moveToPositionAsync(x, y, z, velocity)
        else:  # no
            self.client.moveToPositionAsync(x, y, z, velocity).join()
