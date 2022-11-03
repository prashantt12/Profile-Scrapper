from typing import Union, Any
from dateutil.parser import parse

from selenium.common import NoSuchElementException

from ScrappingEngine.driver import Driver
from ScrappingEngine.ScrappingUtils import Scraping_utilities


from selenium.webdriver.common.by import By
from seleniumwire import webdriver


class TweetFinder:
    _tweet: webdriver.Chrome

    def __init__(self, driver: Driver) -> None:
        self._tweet = driver.driver

    def FindAllTweets(self) -> list[Any]:
        """Finds all tweets from the page"""
        try:
            return self._tweet.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
        except Exception as ex:
            print(f"Error at method fetch_all_tweets : {ex}")
            return []


class ContentFinder(TweetFinder):
    def find_replies(self) -> Union[int, str]:
        """finds replies from the tweet"""
        try:
            replies_element = self._tweet.find_element(
                By.CSS_SELECTOR, '[data-testid="reply"]')
            replies = replies_element.get_attribute("aria-label")
            return Scraping_utilities.extract_digits(replies)
        except Exception as ex:
            print("Error at method find_replies : {}".format(ex))
            return ""

    def find_shares(self) -> Union[int, str]:
        """finds shares from the self._tweet"""
        try:
            shares_element = self._tweet.find_element(
                By.CSS_SELECTOR, '[data-testid="retweet"]')
            shares = shares_element.get_attribute("aria-label")
            return Scraping_utilities.extract_digits(shares)
        except Exception as ex:
            print("Error at method find_shares : {}".format(ex))
            return ""

    def find_status(self) -> Union[list, tuple]:
        """finds status and link from the self._tweet"""
        try:
            anchor = self._tweet.find_element(
                By.CSS_SELECTOR, "a[aria-label][dir]")
            return (anchor.get_attribute("href").split("/"), anchor.get_attribute("href"))
        except Exception as ex:
            print("Error at method find_status : {}".format(ex))
            return []

    def find_all_anchor_tags(self) -> Union[list, None]:
        """finds all anchor tags from the self._tweet"""
        try:
            return self._tweet.find_elements(By.TAG_NAME, 'a')
        except Exception as ex:
            print(
                "Error at method find_all_anchor_tags : {}".format(ex))

    def find_timestamp(self) -> Union[str, None]:
        """finds timestamp from the self._tweet"""
        try:
            timestamp = self._tweet.find_element(By.TAG_NAME,
                                           "time").get_attribute("datetime")
            posted_time = parse(timestamp).isoformat()
            return posted_time
        except Exception as ex:
            print("Error at method find_timestamp : {}".format(ex))

    def find_content(self) -> Union[str, None]:
        try:
            #content_element = self._tweet.find_element('.//*[@dir="auto"]')[4]
            content_element = self._tweet.find_element(By.CSS_SELECTOR, 'div[lang]')
            return content_element.text
        except NoSuchElementException:
            return ""
        except Exception as ex:
            print("Error at method find_content : {}".format(ex))

    def find_like(self) -> Union[int, None]:
        """finds the like of the self._tweet"""
        try:
            like_element = self._tweet.find_element(
                By.CSS_SELECTOR, '[data-testid="like"]')
            likes = like_element.get_attribute("aria-label")
            return Scraping_utilities.extract_digits(likes)
        except Exception as ex:
            print("Error at method find_like : {}".format(ex))

    def find_images(self) -> Union[list, None]:
        """finds all images of the self._tweet"""
        try:
            image_element = self._tweet.find_elements(By.CSS_SELECTOR,
                                                'div[data-testid="self._tweetPhoto"]')
            images = []
            for image_div in image_element:
                href = image_div.find_element(By.TAG_NAME,
                                              "img").get_attribute("src")
                images.append(href)
            return images
        except Exception as ex:
            print("Error at method find_images : {}".format(ex))
            return []

    def find_videos(self) -> list:
        """finds all videos present in the self._tweet"""
        try:
            image_element = self._tweet.find_elements(By.CSS_SELECTOR,
                                                'div[data-testid="videoPlayer"]')
            videos = []
            for video_div in image_element:
                href = video_div.find_element(
                    By.TAG_NAME, "video").get_attribute("src")
                videos.append(href)
            return videos
        except Exception as ex:
            print("Error at method find_videos : {}".format(ex))
            return []

    def is_re_tweet(self) -> bool:
        """return if the self._tweet is whether re-tweet"""
        try:
            self._tweet.find_element(By.CSS_SELECTOR, 'div.r-92ng3h.r-qvutc0')
            return True
        except NoSuchElementException:
            return False
        except Exception as ex:
            print("Error at method is_retweet : {}".format(ex))
            return False

    def find_name_from_tweet(self, is_re_tweet=False) -> Union[str, None]:
        """finds the name from the post"""
        try:
            name = "NA"
            anchors = self.find_all_anchor_tags()
            if len(anchors) > 2:
                if is_re_tweet:
                    name = self._tweet.find_element(
                        By.CSS_SELECTOR, '[data-testid="User-Names"] > div a').text
                else:
                    name = anchors[1].text.split("\n")[0]
            return name
        except Exception as ex:
            print(
                "Error at method find_name_from_post : {}".format(ex))

    def find_external_link(self) -> Union[str, None]:
        """finds external link from the self._tweet"""
        try:
            card = self._tweet.find_element(
                By.CSS_SELECTOR, '[data-testid="card.wrapper"]')
            href = card.find_element(By.TAG_NAME, 'a')
            return href.get_attribute("href")

        except NoSuchElementException:
            return ""
        except Exception as ex:
            print(
                "Error at method find_external_link : {}".format(ex))

    def find_profile_image_link(self) -> Union[str, None]:
        """finds profile image links

        Args:
            self._tweet: Tweet Element

        Returns:
            Union[str, None]: returns string containing image link.
        """
        try:
            return self._tweet.find_element(By.CSS_SELECTOR, 'img[alt][draggable="true"]').get_attribute('src')
        except Exception as ex:
            print("Find Profile Image Link : {}".format(ex))
