import sys  # for exceptions class that we defined earlier 
import pandas as pd, numpy as np
from typing import Optional    #for type hinting in python

from src.exception import exceptions
from src.constants import DATABASE_NAME
from src.configuration.mongo_db_connection import MongoDBClient


class Proj1_data:
    "This class will extract data files from mongoDB and export as DataFrame"

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise exceptions(e,sys)
        
    def export_collection_as_DF(self, collection_name:str, database_name:Optional[str]=None) -> pd.DataFrame:
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]

            #Convert collection data to DataFrame and essential preprocessing at the same time
            print("Fetching data from MongoDB")
            df = pd.DataFrame(list(collection.find()))
            print(f'Data fetched with length of {len(df)}')
            
            if 'id' in df.columns:
                df.drop(columns=['id'])
            df.replace({'na',np.nan}, inplace=True)
            return df

        except Exception as e:
            raise exceptions(e, sys)