from typing import Callable, Any

from selenium.common import WebDriverException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver

from ScrappingEngine.driver import Driver
from ScrappingEngine.driver_utils import DriverUtils

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TwitterDriverUtils(DriverUtils):
    @staticmethod
    def WaitUntil(driver: Driver, time: float, method: Callable[[webdriver.Chrome], Any], message: str = "") -> None:
        try:
            WebDriverWait(driver.driver, time).until(method, message)
        except TimeoutException:
            # log waited but nothing happened
            pass

    @staticmethod
    def WaitUntilNot(driver: Driver, time: float, method: Callable[[webdriver.Chrome], Any], message: str = "") -> None:
        try:
            WebDriverWait(driver.driver, time).until_not(method, message)
        except TimeoutException:
            # log waiting but did not stop
            pass

    @staticmethod
    def WaitForTweets(driver: Driver) -> None:
        TwitterDriverUtils.WaitUntil(driver, 10, EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="tweet"]')))

    @staticmethod
    def wait_until_tweets_appear(driver: Driver) -> None:
        """Wait for tweet to appear. Helpful to work with the system facing
        slow internet connection issues
        """
        try:
            TwitterDriverUtils.WaitUntil(driver, 10, EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="tweet"]')))
        except WebDriverException:
            print(
                "Tweets did not appear!, Try setting headless=False to see what is happening")
