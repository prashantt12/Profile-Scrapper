from ScrappingEngine.driver import Driver, Browser

from TwitterScrapping.twitter_engine import TwitterEngine


def main() -> None:
    t: TwitterEngine = TwitterEngine(Driver(Browser()))
    t.FetchData()
    t.Save()


if __name__ == "__main__":
    main()
