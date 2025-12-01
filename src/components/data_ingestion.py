import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

from src.entity.config_entity import Data_Ingestion_config
from src.entity.artifact_entity import Data_Ingestion_artifact
from src.exception import exceptions
from src.logger import logging
from src.data_access.proj1_data import Proj1_data



class DataIngestion:
    def __init__(self, data_ingestion_config:Data_Ingestion_config = Data_Ingestion_config()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise exceptions(e,sys)
        

    def export_data(self):
        "This method will save data sets from mongoDB to your local storage and return the Df"

        try:
            logging.info("Exporting data from mongoDB")
            data_object = Proj1_data()
            Df = data_object.export_collection_as_DF(collection_name = self.data_ingestion_config.collection_name)
            logging.info('Shape of tha DataFrame{Df.shape}')

            data_save_file_path = self.data_ingestion_config.data_save_file_path
            dir_path = os.path.dirname(data_save_file_path)    #extracts only dir filepath from full filepath
            os.makedirs(dir_path, exist_ok=True)
            logging.info("Saving data into this filepath  : {data_save_file_path}")
            Df.to_csv(data_save_file_path,index=False)
            return Df
        
        except Exception as e:
            raise exceptions(e,sys)
        

    def Train_test_split(self,Df:pd.DataFrame):
        logging.info("Entered Train_test_split method of DataIngestion class")

        try:
            train_set, test_set = train_test_split(Df, test_size=self.data_ingestion_config.train_test_split_ratio, shuffle=True, random_state=6)
            logging.info("Performed train test split on the dataframe")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path.")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False)
            logging.info(f"Exported train and test file path.")

        except Exception as e:
            raise exceptions(e,sys)


    def initiate_data_ingestion(self)->None:
        try:
            logging.info("Fetching data from MongoDB ...")
            df = self.export_data()
            logging.info("Data Exported!")

            self.Train_test_split(df)
            logging.info("Train & Test data sets has been saved")

            data_ingestion_artifact = Data_Ingestion_artifact(training_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.testing_file_path)
            
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise exceptions(e, sys) from e
