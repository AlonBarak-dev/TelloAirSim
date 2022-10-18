import threading
import time
import logging


class LoggerThread(threading.Thread):
    """
    A Thread class to handle the logging of the program to file
    """

    def __init__(self, client=None):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.client = client

        #  Initiating logger -->
        self.logger = logging.getLogger("mainLogger")
        self.logger.setLevel(logging.DEBUG)
        f_handler = logging.FileHandler('log.log', 'w', encoding="utf-8")
        logFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(logFormat)
        self.logger.addHandler(f_handler)  # <--

        self.logger.info("Logging initiated")

    def stop(self):
        """
        Method to be called when the thread should be stopped
        :return: 
        """""
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        """
        Method to be executed by the thread. Logs info from Airsim
        :return:
        """
        while not self.stopped():  # Thread stops upon call to stop() method above
            state = self.client.getMultirotorState()  # Get Airsim state data
            collision = self.client.simGetCollisionInfo()  # Get Airsim collision data
            self.logger.info("State:\n" + str(state))
            self.logger.info("Collision:\n" + str(collision))
            time.sleep(1)

    def getLogger(self):
        """
        Simple getter method to allow logging from outside the class
        :return: logger
        """
        return self.logger
