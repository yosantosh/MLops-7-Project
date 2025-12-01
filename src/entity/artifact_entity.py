from dataclasses import dataclass # to store data essentially in class 

@dataclass
class Data_Ingestion_artifact:
    training_file_path :str 
    test_file_path:str