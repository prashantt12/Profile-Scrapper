from time import sleep
from random import randint

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .driver import Driver


class DriverUtils:
    @staticmethod
    def WaitForLoad(driver: Driver) -> None:
        status = False
        while not status:
            sleep(randint(3, 5))
            status = driver.ExecuteJS("return document.readyState")

    @staticmethod
    def scroll_down(driver) -> None:
        """Helps to scroll down web page"""
        try:
            body = driver.find_element(By.CSS_SELECTOR, 'body')
            for _ in range(randint(1, 3)):
                body.send_keys(Keys.PAGE_DOWN)
        except Exception as ex:
            print("Error at scroll_down method {}".format(ex))

    @staticmethod
    def wait_until_completion(driver) -> None:
        """waits until the page have completed loading"""
        try:
            state = False
            while not state:
                sleep(randint(3, 5))
                state = driver.ExecuteJS("return document.readyState")
        except Exception as ex:
            print('Error at wait_until_completion: {}'.format(ex))
