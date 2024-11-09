import datetime
from pathlib import Path
import pandas as pd
import datetime

from datamanagement.datafetch.news import NewsORGAPI, WorldNewsAPI
from datamanagement.datapreprocessing.model_config import model_configuration
from datamanagement.database.db_load import create_and_insert_to_db
from datamanagement.datawarehouse.data_load import load_sqlite_to_bigquery
from datamanagement.datapreprocessing.data_cleaning import clean_historical_news
from datamanagement.datapreprocessing.data_transforming import (create_features_from_pretrained_models
                                                                ,retrieve_counts_on_part_of_speech)

from datamanagement.data.read_data import retrieve_live_data

# This is used in the apache kafka
# retrieve_live_data('v1-realtime_data')

# df = pd.read_csv("./datamanagement/data/final_history_data.csv")
# df = clean_historical_news(df)
# new_df = create_features_from_pretrained_models(model_configuration,
#                                                 df,
#                                                 [
#                                                  "article_content",
#                                                  "article_title",
#                                                  "article_description"])
# new_df.to_csv("./datamanagement/data/latest_today_transformation.csv", index=False)

# get_historical_data("historical_news_data123")


# date_30_days_ago = datetime.datetime.today() - datetime.timedelta(days=31)
# date_30_days_ago_str = date_30_days_ago.strftime("%Y-%m-%d")

# try:
#     historical_data = world_news_api.retrieve_historical_data(
#                         offset=0,
#                         categories=WORLD_NEWS_CATEGORIES,
#                         start_date="2024-06-01",
#                         end_date="2024-07-01",
#                         n_post=2000
#                         )
#     historical_data.to_csv("datamanagement/data/all_categories-2024-06-01-2024-07-01.csv")
# except Exception as oops:
#     print(f"Error occurred while storing historical data as {oops}")



def historical_pipeline(csv_path="datamanagement\data\merged_output.csv"):
    # Load the final csv file
    df = pd.read_csv(csv_path)
    print(df.columns)
    print(df.shape)
    # Clean that
    clean_df = clean_historical_news(df)
    print(clean_df.columns)
    print(clean_df.shape)
    # Transform pOS count
    transformed_df = retrieve_counts_on_part_of_speech(
                clean_df,
                columns=["article_content", "article_description", "article_title"])
    print(transformed_df.columns)
    print(transformed_df.shape)
    transformed_df.to_csv("transformed_data.csv")
    # Create a function for database and call it
    create_and_insert_to_db(transformed_df,db_name="newsdb")
    # Create a function to insert into bigquery and call it
    load_sqlite_to_bigquery('news_database.db', 'newsanalytics-440610-81d148518740.json', 'newsanalytics-440610', 'testnews')

#historical_pipeline()
# transformed_df = pd.read_csv("historical_transormed.csv")
# main(transformed_df,db_name="newsdb1")
JSON_FILE = "newsanalytics-440610-81d148518740.json"
PROJECT_ID = "newsanalytics-440610"
# DATASET_NAME = "testnews1"
# load_sqlite_to_bigquery('newsdb1.db', JSON_FILE, PROJECT_ID, DATASET_NAME)

df = retrieve_live_data("hello")
df.to_csv('hello.csv')
print(df.head())
historical_pipeline("hello.csv")