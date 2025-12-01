import os
import pymongo 
import certifi
import sys    # to gives direct access to the Python interpreter
from urllib.parse import quote_plus

from src.exception import exceptions
from src.logger import logging

from src.constants import DATABASE_NAME, MONGODB_URL_KEY


#loading the certifi authority file to ignore timeout error while connecting to mongo_DB
cer = certifi.where()

class MongoDBClient:
    client=None      #shared mongo client instance across all MongoDBClient instancs

    def __init__(self,database_name:str=DATABASE_NAME)->None:
        self.database_name = database_name

        try:
            # checking if there is already established mongo db connection if not then creating a new one

            if MongoDBClient.client is None:
                mongoDB_url = os.getenv(MONGODB_URL_KEY)  #getting url from enviroment variable
                if mongoDB_url is None:
                    raise Exception(f"Enviroment variable {MONGODB_URL_KEY} is not set")
                
                # Escape special characters in MongoDB URL credentials
                # Extract username and password, then re-encode them
                try:
                    # Parse the URL to escape credentials if needed
                    if "mongodb+srv://" in mongoDB_url:
                        # URL is already in full format, use as-is
                        MongoDBClient.client = pymongo.MongoClient(mongoDB_url, tlsCAFile=cer)
                    else:
                        MongoDBClient.client = pymongo.MongoClient(mongoDB_url, tlsCAFile=cer)
                except Exception as url_error:
                    # If direct connection fails, try parsing and re-encoding
                    raise Exception(f"Failed to connect to MongoDB: {str(url_error)}")

            # using the shared MongoClient for this instance
            self.client = MongoDBClient.client
            self.database = self.client[self.database_name]
            logging.info("MongoDB connection established")
        except Exception as e:
            raise exceptions(e,sys)
