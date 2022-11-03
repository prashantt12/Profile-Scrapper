from ScrappingEngine.driver import Browser, Driver

from typing import Union


class ScrappingEngine:
    driver: Union[Driver, None] = None
    url: str = ""

    def __init__(self, scrape_url: str, driver: Driver = Driver(Browser())) -> None:
        self.driver = driver
        self.url = scrape_url
        self.driver.Connect(self.url)

