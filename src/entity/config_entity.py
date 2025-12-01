import os
from dataclasses import dataclass
from datetime import datetime

from src.constants import *    # import everything written in __init__.py

time_now = datetime.now().strftime("%d_%m_%y__%H_%M_%S")

@dataclass
class Training_pipeline_config:
    pipeline_name :str = PIPELINE_NAME
    artifact_dir : str = ARTIFACT_DIR
    timestamp :str = time_now

training_pipeline_config: Training_pipeline_config = Training_pipeline_config()


@dataclass
class Data_Ingestion_config:
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
    data_save_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    training_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    testing_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name:str = DATA_INGESTION_COLLECTION_NAME
