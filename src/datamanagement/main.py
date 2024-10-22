import datetime
from pathlib import Path
from datafetch.news import NewsORGAPI, WorldNewsAPI
# from .datapreprocessing

NEWS_CATEGORIES = ["Politics", "Business & Economy", "Technology", "Health",
    "Science","Sports", "Entertainment", "Environment", "Education", "World/International News",
    "Local News", "Lifestyle", "Crime & Law", "Weather", "Arts & Culture",
    "Travel", "Opinion/Editorials", "Fashion", "Real Estate", "Food & Dining",
    "History", "Social Issues", "Automotive"]
CATEGORIES =  ["business","entertainment","general","health","science","sports","technology"]
COUNTRY_CODES_BASED_ON_CONTINENTS = ["ke", "ng", "cn", "in",
                                    "ru", "de", "uk", "ca", "us",
                                    "ir", "jp", "tw", "sg" ]

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
        historical_df.to_csv(f"./data/{pre_output_filename}{date_30_days_ago_str}.csv")
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
    NEWS_API_FILENAME = \
        f"./datamanagement/data/{pre_output_filename}-news-api-{current_date}.csv"
    WORLD_NEWS_API_FILENAME = \
        f"./datamanagement//data/{pre_output_filename}-world-news-api-{current_date}.csv"
    try:
        # Retrieve the data from world news API
        historical_df = world_news_api.retrieve_real_time_data(
                                    country_codes=COUNTRY_CODES_BASED_ON_CONTINENTS,
                                    language_code="en")
        # Store the data into a csv file
        historical_df.to_csv(WORLD_NEWS_API_FILENAME)
    except Exception as oops:
        print(f"Error occurred while storing historical data with" +
               "World News API  as {oops}")
    try:
        # Retrieve the data from news API
        df = news_api.retrieve_real_time_data(categories=CATEGORIES)
        # Store the data into a csv file
        df.to_csv(NEWS_API_FILENAME)
    except Exception as oops:
        print(f"Error occurred while storing realtime data with newsapi as {oops}")

    # Whether the file is stored successfully
    if (Path(NEWS_API_FILENAME).exists() and \
        (Path(WORLD_NEWS_API_FILENAME).exists())):
        return True
    return False

# This is used in the apache kafka
# retrieve_live_data('v1-realtime_data')