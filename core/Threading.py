import threading
import time

"""Taken from http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/"""
class Threading(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1, function=None, args=None):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=(function, args))
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self, function, args):
        """ Method that runs forever """
        function(args)

