import calendar
import os
import keyboard
import pyautogui
from collections.abc import Callable
from time import sleep
from datetime import datetime, timedelta


class TabListener:

    def __init__(self, timeout: timedelta = timedelta(seconds=5), save_location: str = 'game-data\\tmp'):
        """
        Constructor for the TabListener class
        :param timeout: how long to wait between screenshots if tab is held
        :param save_location: location to save the screenshots to
        """
        self.timeout = timeout
        self.last_press = datetime.fromtimestamp(0)
        self.save_location = save_location

    def take_screenshot(self):
        """
        Takes a screenshot and saves it to the save location
        :return: None
        """
        # create a tmp folder in game data if one does not already exist
        if not os.path.exists(self.save_location):
            os.makedirs(self.save_location)

        # get timestamp for picture name
        date = datetime.utcnow()
        utc_time = calendar.timegm(date.utctimetuple())

        # take screenshot and save it to the tmp folder
        sleep(0.5)
        screenshot = pyautogui.screenshot()
        screenshot.save(f'{self.save_location}\\{utc_time}.png')

    def overload_handler(self, timeout: timedelta, callback: Callable, args: tuple = (), kwargs: dict = {}):
        """
        Function to handle too many calls to a function. Keyboard listener records pressing a button as
        multiple presses so this function handles that with a set-able timeout
        :param timeout: amount of time allowed between function calls
        :param callback: function to run
        :param args: positional arguments for the function
        :param kwargs: key word arguments to call the function with
        :return: None
        """
        time = datetime.now()
        if time - self.last_press > timeout:
            callback(*args, **kwargs)
        self.last_press = time

    def listen(self):
        """
        Listens forever for tab presses.
        When the tab key is pressed it will take a screenshot and save it to specified folder
        :return: None
        """
        keyboard.add_hotkey('tab', self.overload_handler, (self.timeout, self.take_screenshot))
        keyboard.wait()


if __name__ == "__main__":
    print("Overwatch stats collector started!")
    print("Pressing tab will save a screenshot to game-data\\tmp")
    print("press CTRL-C to quit")
    tl = TabListener()
    tl.listen()
