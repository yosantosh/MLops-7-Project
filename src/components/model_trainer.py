from typing import Tuple
import numpy as np

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from xgboost import XGBClassifier

import sys
from src.exception import exceptions
from src.logger import logging 
from src.utils.main_utils import load_numpy_array_data, load_object, save_object
from src.entity.config_entity import ModelTrainerConfig, XGBoostConfig
from src.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ClassificationMetricArtifact
from src.entity.estimator import MyModel


class ModelTrainer:
    def __init__(self,data_transformation_artifact: DataTransformationArtifact,model_trainer_config: XGBoostConfig):
        """
        Docstring for __init__
        
        :param self: Description
        :param data_transformation_artifact: Reference of Data Transformation stage completion.
        :type data_transformation_artifact: DataTransformationArtifact
        :param model_trainer_config: Stored config/variables for model trainer stage
        :type model_trainer_config: XGBoostConfig
        """

        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self,train:np.array,test:np.array) -> Tuple[object,object]:
        """
        This method will return the model object after training and classification report
        
        :param train: X_train and y_train array
        :type train: np.array
        :param test: X_test and y_test array
        :type test: np.array
        """

        try:
            logging.info("Training XGBoost model with specified hyperparameters")

            # splitting train & test
            X_train,y_train, X_test,y_test = train[:,:-1],train[:,-1],test[:,:-1],test[:,-1]
            logging.info("Train and Test data split is done")

            #initializing model object
            model = XGBClassifier(
                learning_rate = self.model_trainer_config.learning_rate,
                n_estimators = self.model_trainer_config.n_estimators,
                max_depth = self.model_trainer_config.max_depth,
                min_child_weight = self.model_trainer_config.min_child_weight,
                gamma = self.model_trainer_config.gamma,
                subsample = self.model_trainer_config.subsample,
                colsample_bytree = self.model_trainer_config.colsample_bytree,
                objective = self.model_trainer_config.objective,
                nthread = self.model_trainer_config.nthread,
                scale_pos_weight = self.model_trainer_config.scale_pos_weight,
                seed = self.model_trainer_config.seed,
                random_state = self.model_trainer_config.random_state
            )
	            

            logging.info("Fitting the model object with training data")
            model.fit(X_train,y_train)
            logging.info("Model is trained successfully")

            #prediction and evaluating model performance metrices
            y_pred = model.predict(X_test)
            accoracy = accuracy_score(y_test,y_pred)
            f1 = f1_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)

            # creating matrix artifact object
            metric_artifact = ClassificationMetricArtifact(f1_score=f1,precision_score=precision,recall_score=recall)
            return model,metric_artifact
        
        except Exception as e:
            raise exceptions(e, sys) from e
        

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        """
        Method Name :   initiate_model_trainer
        Description :   This function initiates the model training steps
        
        Output      :   Returns model trainer artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            print("------------------------------------------------------------------------------------------------")
            print("Starting Model Trainer Component")
            # Load transformed train and test data
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
            logging.info("train-test data loaded")
            
            # Train model and get metrics
            trained_model, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)
            logging.info("Model object and artifact loaded.")
            
            # Load preprocessing object
            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            logging.info("Preprocessing obj loaded.")

            # Check if the model's accuracy meets the expected threshold
            if accuracy_score(train_arr[:, -1], trained_model.predict(train_arr[:, :-1])) < self.model_trainer_config.expected_accuracy:
                logging.info("No model found with score above the base score")
                raise Exception("No model found with score above the base score")

            # Save the final model object that includes both preprocessing and the trained model
            logging.info("Saving new model as performace is better than previous one.")
            my_model = MyModel(preprocessing_object=preprocessing_obj, trained_model_object=trained_model)
            save_object(self.model_trainer_config.trained_model_file_path, my_model)
            logging.info("Saved final model object that includes both preprocessing and the trained model")

            # Create and return the ModelTrainerArtifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact,
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        
        except Exception as e:
            raise exceptions(e, sys) from e