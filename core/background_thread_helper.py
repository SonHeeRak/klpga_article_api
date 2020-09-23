import threading
import atexit
import config as c
from core.log_helper import LogHelper
import sys
import datetime


is_init = False

try:
    POOL_TIME = int(c.SERVER_CONFIG['background_thread_time'])
    START_TIME = int(c.SERVER_CONFIG['background_thread_start_hour'])
    END_TIME = int(c.SERVER_CONFIG['background_thread_end_hour'])
except Exception as e:
    LogHelper.instance().e(e, file_name=sys._getframe().f_code.co_filename,
                           func_name=sys._getframe().f_code.co_name)
    POOL_TIME = 60 * 60 * 3
    START_TIME = 2
    END_TIME = 6

dataLock = threading.Lock()
yourThread = threading.Thread()

callbackFunction = None


def interrupt():
    global yourThread
    yourThread.cancel()


def do_stuff():
    global yourThread
    global callbackFunction
    global is_init

    with dataLock:
        if callbackFunction is not None:
            try:
                if is_init:
                    now_hour = int(datetime.datetime.now().strftime('%H'))

                    if START_TIME <= now_hour < END_TIME:
                        callbackFunction()
                else:
                    is_init = True
                    callbackFunction()
            except Exception as ex:
                LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                       func_name=sys._getframe().f_code.co_name)

    yourThread = threading.Timer(POOL_TIME, do_stuff, ())
    yourThread.start()


def do_stuff_start():
    global yourThread

    yourThread = threading.Timer(10, do_stuff, ())
    yourThread.start()


class BackgroundThreadHelper:
    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = BackgroundThreadHelper()
        return cls.__instance

    def __init__(self):
        print('background_thread_helper init')

    def run(self, callback=None):
        global callbackFunction

        if callback is not None:
            callbackFunction = callback
            #callbackFunction()

        do_stuff_start()
        atexit.register(interrupt)


