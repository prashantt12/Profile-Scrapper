from dataclasses import dataclass
from typing import Union, Callable, Any

from .utils.singleton import Singleton

# selenium imports
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver

from fake_headers import Headers


@dataclass
class Browser:
    name: str = "Chrome"
    proxy: str = ""
    headless: bool = False
    headers: Headers = Headers().generate()['User-Agent']
    profile: Union[str, None] = None


class Driver(metaclass=Singleton):
    __browser: Union[Browser, None] = None
    __proxy: str = None
    driver: Union[webdriver.Chrome, None] = None
    headless: bool = False

    def __init__(self, browser_config: Browser) -> None:
        self.__browser = browser_config
        self.__initDriver()

    def Connect(self, url: str):
        self.driver.get(url)

    def ExecuteJS(self, script: str) -> bool:
        try:
            self.driver.execute_script(script)
            return True
        except KeyError:
            # log error in javascript (script)
            return False

    def __initDriver(self) -> None:
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                       options=self.__setProperties())

    def __setProperties(self) -> webdriver.ChromeOptions:
        browser_option: webdriver.ChromeOptions = webdriver.ChromeOptions()

        if self.headless:
            browser_option.add_argument("--headless")
        if self.__browser.profile and self.__browser.name.lower() == "chrome":
            browser_option.add_argument(
                f"user-data-dir={self.__browser.profile}")
        if self.__browser.profile and self.__browser.name.lower() == "firefox":
            browser_option.add_argument("-profile")
            browser_option.add_argument(self.__browser.profile)

        browser_option.add_argument('--no-sandbox')
        browser_option.add_argument("--disable-dev-shm-usage")
        browser_option.add_argument('--ignore-certificate-errors')
        browser_option.add_argument('--disable-gpu')
        browser_option.add_argument('--log-level=3')
        browser_option.add_argument('--disable-notifications')
        browser_option.add_argument('--disable-popup-blocking')
        browser_option.add_argument(
            f'--user-agent={self.__browser.headers.__str__()}')

        return browser_option
