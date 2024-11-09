import os
from pathlib import Path
import pandas as pd
import datetime

from datamanagement.datafetch.news import NewsORGAPI, WorldNewsAPI

def read_top_data():

    current_file_path = Path(__file__).resolve()
    current_directory = current_file_path.parent
    file_path = Path(current_directory) / "all_categories-2024-06-01-2024-07-01.csv"
    df = pd.read_csv(file_path)
    return df.head()




NEWS_CATEGORIES = ["Politics", "Business & Economy", "Technology", "Health",
    "Science","Sports", "Entertainment", "Environment", "Education", "World/International News",
    "Local News", "Lifestyle", "Crime & Law", "Weather", "Arts & Culture",
    "Travel", "Opinion/Editorials", "Fashion", "Real Estate", "Food & Dining",
    "History", "Social Issues", "Automotive"]
CATEGORIES =  ["business","entertainment","general","health","science","sports","technology"]
COUNTRY_CODES_BASED_ON_CONTINENTS = ["us"]

WORLD_NEWS_CATEGORIES = ["politics", "sports", "business", "technology", "entertainment", "health", "science", "lifestyle", "travel", "culture", "education","environment", "other"]
news_api = NewsORGAPI()
world_news_api = WorldNewsAPI()

def get_historical_data(pre_output_filename:
                         str = "historical_news_data"):
    """ Retrieve news data from previous month using NewsAPI and 
    stores a csv file in the data folder with pre_output_filename given

    Arguments: 

        - pre_output_filename: the prefix file name to be stored as
        
    Returns: 

        - bool: True when it's successfully stored else false

    """
    # Format of date in YYYY-MM-DD
    date_30_days_ago = datetime.datetime.today() - datetime.timedelta(days=30)
    date_30_days_ago_str = date_30_days_ago.strftime("%Y-%m-%d")
    try:
        historical_df = news_api.retrieve_past_data_for_category(
                        from_date=date_30_days_ago_str,
                        categories=NEWS_CATEGORIES)
        historical_df.to_csv(f"./datamanagement/data/{pre_output_filename}{date_30_days_ago_str}.csv")
        return True
    except Exception as oops:
        print(f"Error occurred while storing historical data as {oops}")
        return False


def retrieve_live_data(pre_output_filename:
                         str = "real-time-data"):
    """ Retrieve live news data from News API & World News API and 
    store it with the prefix name given with pre_output_filename

    Arguments: 

        - pre_output_filename: the prefix file name to be stored as
        
    Returns: 

        - bool: True when it's successfully stored else false

    """
    # Retrieve current date information in the string format
    current_date = datetime.datetime.today().strftime("%Y-%m-%d")   
    # File path for the csv files
    # NEWS_API_FILENAME = \
    #     f"./datamanagement/data/{pre_output_filename}-news-api-{current_date}.csv"
    # WORLD_NEWS_API_FILENAME = \
    #     f"./datamanagement//data/{pre_output_filename}-world-news-api-{current_date}.csv"
    NEWS_API_FILENAME = \
        f"./{pre_output_filename}-news-api-{current_date}.csv"
    WORLD_NEWS_API_FILENAME = \
        f"./{pre_output_filename}-world-news-api-{current_date}.csv"

    df = pd.DataFrame()
    try:
        # Retrieve the data from world news API
        realtime_data = world_news_api.retrieve_real_time_data(
                                    country_codes=COUNTRY_CODES_BASED_ON_CONTINENTS,
                                    language_code="en")
        # Store the data into a csv file
        # realtime_data.to_csv(WORLD_NEWS_API_FILENAME)
        df = pd.concat([df,realtime_data])
    except Exception as oops:
        print("Error occurred while storing historical data with" +
              f"World News API  as {oops}")
    try:
        # Retrieve the data from news API
        real_data = news_api.retrieve_real_time_data(categories=CATEGORIES)
        # Store the data into a csv file
        df = pd.concat([df,real_data])

        # df.to_csv(NEWS_API_FILENAME)
    except Exception as oops:
        print(f"Error occurred while storing realtime data with newsapi as {oops}")

    return df


df = retrieve_live_data("hello")
print(df.head())