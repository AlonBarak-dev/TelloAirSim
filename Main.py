import airsim
import logging

from LoggerThread import LoggerThread
from Server_ControlDrone import ServerThread

if __name__ == '__main__':
    serverThread = ServerThread()  # Initiating connection to clientPC

    client: airsim.MultirotorClient = serverThread.client
    loggerThread = LoggerThread(client)  # Initiate logger class instance
    logger: logging.Logger = loggerThread.getLogger()  # Getting logger from the loggerThread instance
    serverThread.logger = logger  # Assignment of logger to server thread (to be able to log from it to the same file and with the same settings)

    logger.info("Connected to instance of Airsim, simulation ready to start...")  # Logging

    loggerThread.start()  # Start continuous logging to appropriate file and console
    serverThread.start()  # Start continuous receiving of commands to the drone

    serverThread.join()
    loggerThread.stop()
