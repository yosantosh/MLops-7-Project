"""

File: src/entity/artifact_entity.py — defines the project’s artifact entity/type.

Purpose: represents an artifact (model, dataset, metric, etc.) and its metadata so 
    components can pass, log, and persist artifacts consistently.

Typical contents: a dataclass or class like Artifact with fields such as uri/path, type,
    version, size, checksum, created_at, plus helpers for validation/serialization.

Used by: pipeline steps, loggers (MLflow/etc.), storage adapters, and any code that needs structured artifact metadata.


"""
from dataclasses import dataclass # to store data essentially in class 

@dataclass
class Data_Ingestion_artifact:
    training_file_path :str 
    test_file_path:str


@dataclass
class DataValidationArtifact:
    validation_status:bool         # at the end of validation we will get true or false 
    message: str                   # to give some info regarding validation
    validation_report_file_path: str # path where report is saved



@dataclass
class DataTransformationArtifact:
    transformed_object_file_path:str 
    transformed_train_file_path:str
    transformed_test_file_path:str

# @dataclass
# class ClassificationMetricArtifact:
#     f1_score:float
#     precision_score:float
#     recall_score:float

# @dataclass
# class ModelTrainerArtifact:
#     trained_model_file_path:str 
#     metric_artifact:ClassificationMetricArtifact

# @dataclass
# class ModelEvaluationArtifact:
#     is_model_accepted:bool
#     changed_accuracy:float
#     s3_model_path:str 
#     trained_model_path:str

# @dataclass
# class ModelPusherArtifact:
#     bucket_name:str
#     s3_model_path:str