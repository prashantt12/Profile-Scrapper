import csv
import json
import os
from typing import Any
import re

from .twitter_driver_utils import TwitterDriverUtils
from ScrappingEngine.engine import ScrappingEngine
from ScrappingEngine.driver import Driver
from .Finder import ContentFinder


class TwitterEngine(ScrappingEngine):
    __retries: int = 5
    __scrapper: ContentFinder
    __url = "https://www.twitter.com/elonmusk"

    tweets_count = 3
    posts_data = {}
    twitter_username = "elonmusk"

    def __init__(self, driver: Driver) -> None:
        super().__init__(self.__url, driver)
        self.__scrapper = ContentFinder(self.driver)

    def FetchData(self):
        all_ready_fetched_posts = []
        present_tweets = self.__scrapper.FindAllTweets()
        self.__check_tweets_presence(present_tweets)
        all_ready_fetched_posts.extend(present_tweets)

        while len(self.posts_data) < self.tweets_count:
            for tweet in present_tweets:
                status, tweet_url = self.__scrapper.find_status()
                replies = self.__scrapper.find_replies()
                retweets = self.__scrapper.find_shares()
                status = status[-1]
                username = tweet_url.split("/")[3]
                is_retweet = True if self.twitter_username.lower() != username.lower() else False
                name = self.__scrapper.find_name_from_tweet(is_retweet)
                retweet_link = tweet_url if is_retweet is True else ""
                posted_time = self.__scrapper.find_timestamp()
                content = self.__scrapper.find_content()
                likes = self.__scrapper.find_like()
                images = self.__scrapper.find_images()
                videos = self.__scrapper.find_videos()
                hashtags = re.findall(r"#(\w+)", content)
                mentions = re.findall(r"@(\w+)", content)
                profile_picture = self.__scrapper.find_profile_image_link()
                link = self.__scrapper.find_external_link()
                self.posts_data[status] = {
                    "tweet_id": status,
                    "username": username,
                    "name": name,
                    "profile_picture": profile_picture,
                    "replies": replies,
                    "retweets": retweets,
                    "likes": likes,
                    "is_retweet": is_retweet,
                    "retweet_link": retweet_link,
                    "posted_time": posted_time,
                    "content": content,
                    "hashtags": hashtags,
                    "mentions": mentions,
                    "images": images,
                    "videos": videos,
                    "tweet_url": tweet_url,
                    "link": link
                }

            TwitterDriverUtils.scroll_down(self.driver.driver)
            TwitterDriverUtils.wait_until_completion(self.driver)
            TwitterDriverUtils.wait_until_tweets_appear(self.driver)
            present_tweets = self.__scrapper.FindAllTweets()
            present_tweets = [
                post for post in present_tweets if post not in all_ready_fetched_posts]
            self.__check_tweets_presence(present_tweets)
            all_ready_fetched_posts.extend(present_tweets)
            if self.__check_retry() is True:
                break

    def Save(self, output_format: str = "json", filename: str = "output", directory="."):
        if output_format.lower() == "json":
            if filename == '':
                # if filename was not provided then print the JSON to console
                return json.dumps(self.posts_data)
            elif filename != '':
                # if filename was provided, save it to that file
                mode = 'w'
                json_file_location = os.path.join(directory, filename + ".json")
                if os.path.exists(json_file_location):
                    mode = 'r'
                with open(json_file_location, mode, encoding='utf-8') as file:
                    if mode == 'r':
                        try:
                            file_content = file.read()
                            content = json.loads(file_content)
                        except json.decoder.JSONDecodeError:
                            print('Invalid JSON Detected!')
                            content = {}
                        file.close()
                        self.posts_data.update(content)
                        with open(json_file_location, 'w', encoding='utf-8') as file_in_write_mode:
                            json.dump(self.posts_data, file_in_write_mode)
                    print(
                        'Data Successfully Saved to {}'.format(json_file_location))
        elif output_format.lower() == "csv":
            if filename == "":
                filename = self.twitter_username
            json_to_csv(filename=filename, json_data=self.posts_data, directory=directory)

    def PrintData(self):
        data = dict(list(self.posts_data.items())
                    [0:int(self.tweets_count)])
        return data

    def __check_retry(self):
        return self.__retries <= 0

    def __check_tweets_presence(self, tweet_list: list[Any]):
        if len(tweet_list) <= 0:
            self.__retries -= 1


def json_to_csv(filename, json_data, directory):
    os.chdir(directory)  # change working directory to given directory
    # headers of the CSV file
    fieldnames = ['tweet_id', 'username', 'name', 'profile_picture', 'replies',
                  'retweets', 'likes', 'is_retweet', 'retweet_link', 'posted_time', 'content', 'hashtags',
                  'mentions',
                  'images', 'videos', 'tweet_url', 'link']
    mode = 'w'
    if os.path.exists("{}.csv".format(filename)):
        mode = 'a'
    # open and start writing to CSV files
    with open("{}.csv".format(filename), mode, newline='', encoding="utf-8") as data_file:
        # instantiate DictWriter for writing CSV fi
        writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        if mode == 'w':
            writer.writeheader()  # write headers to CSV file
        # iterate over entire dictionary, write each posts as a row to CSV file
        for key in json_data:
            # parse post in a dictionary and write it as a single row
            row = {
                "tweet_id": key,
                "username": json_data[key]['username'],
                "name": json_data[key]['name'],
                "profile_picture": json_data[key]['profile_picture'],
                "replies": json_data[key]['replies'],
                "retweets": json_data[key]['retweets'],
                "likes": json_data[key]['likes'],
                "is_retweet": json_data[key]['is_retweet'],
                "retweet_link": json_data[key]['retweet_link'],
                "posted_time": json_data[key]['posted_time'],
                "content": json_data[key]['content'],
                "hashtags": json_data[key]['hashtags'],
                "mentions": json_data[key]['mentions'],
                "images": json_data[key]['images'],
                "videos": json_data[key]['videos'],
                "tweet_url": json_data[key]['tweet_url'],
                "link": json_data[key]['link']
            }
            writer.writerow(row)  # write row to CSV file
        data_file.close()  # after writing close the file
    print('Data Successfully Saved to {}.csv'.format(filename))
