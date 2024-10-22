""" The functionalities of the WorldNewsAPI
For further details check out https://worldnewsapi.com
"""

import pandas as pd
import os
import requests
from dotenv import load_dotenv
import datetime

load_dotenv()

class WorldNewsAPI:

    WORLD_NEWS_API = os.getenv("WORLD_NEWS_API")
    HEADERS = {
        'x-api-key': WORLD_NEWS_API
    }
    def _format_articles_into_list(self, top_news: dict):
        """ Converts the json from the worldnewsapi.org into the list.

        Arguments: 
            - top_news: A json with all the articles information in it.

        Returns:

        Yields: 
        - tuple: The information of the article such as (source_id, source_name, author_name,
                article_title, article_description, article_urlToImage,
                article_publishedAt, article_content)
        """
        for news in top_news:
            for article in news['news']:
                source_id = article.get("id", None)
                source_name = article.get("author", None)
                author_name = article.get("authors", [None])[0]
                article_title = article.get("title", None)
                article_description = article.get("summary", None)
                article_urlToImage = article.get("image", None)
                article_publishedAt = article.get("publish_date", None)
                article_content = article.get("text", None)

                yield (source_id, source_name, author_name, article_title, 
                            article_description,article_urlToImage,article_publishedAt, article_content)

    def retrieve_real_time_data(self,
                         country_codes: list,
                         language_code: str = "en") -> pd.DataFrame:
        """ Fetch data from all the categories and store it in dataframe

        Arguments: 

            - country_codes: A list of appropriate categories from api
            - language_code: an appropriate language_code to get the news on

        Returns:

            - pd.Dataframe: A pandas Dataframe with the latest news information

        """
        # Create the default pandas dataframe with the features
        df = pd.DataFrame(columns=["source_id", "source_name", "author_name", "article_title",
                 "article_description","article_urlToImage","article_publishedAt", "article_content"])
        # Get the current date in YYYY-MM-DD format
        current_date = datetime.datetime.today().strftime("%Y-%m-%d")
        try:
            # Retrieval of data for specific country
            for country_code in country_codes:
                url = f"https://api.worldnewsapi.com/top-news?source-country={country_code}&language={language_code}&date={current_date}"
                # Make the api call the get the real time news data
                response = requests.get(url, headers=self.HEADERS, timeout=10)
                # Whether the response is successful
                if response.status_code == 200:
                    # news data in json format
                    data = response.json()
                    top_news = data.get("top_news", [])
                    # articles from the api are converted to the list
                    converted_articles = list(self._format_articles_into_list(top_news))
                    # Create a new Dataframe with converted list
                    new_df = pd.DataFrame(data=converted_articles, 
                            columns=["source_id", "source_name", "author_name", "article_title",
                            "article_description","article_urlToImage","article_publishedAt",
                             "article_content"])
                    # Concat the default dataframe with the new dataframe
                    df = pd.concat([df, new_df])
        except Exception as oops:
            print(f"Error occurred while retrieval of real time data as {oops}")
        return df


if __name__ == "__main__":
    country_codes_based_on_continents = ["ke", "ng", "cn", "in",
                                        "ru", "de", "uk", "ca", "us",
                                        "ir", "jp", "tw", "sg" ]
    world_news_api = WorldNewsAPI()
    try:
        historical_df = world_news_api.retrieve_real_time_data(
                                                 country_codes=country_codes_based_on_continents,
                                                 language_code="en"
                                                 )
        historical_df.to_csv("realtime_world_news.csv")
    except Exception as oops:
        print(f"Error occurred while storing historical data as {oops}")
