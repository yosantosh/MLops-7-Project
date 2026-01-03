import sys
from src.entity.config_entity import VehiclePredictorConfig
from src.entity.s3_estimator import Proj1Estimator
from src.exception import exceptions
from src.logger import logging
import pandas as pd
from pandas import DataFrame


class VehicleData:
    def __init__(self,
                Gender,
                Age,
                Driving_License,
                Region_Code,
                Previously_Insured,
                Annual_Premium,
                Policy_Sales_Channel,
                Vintage,
                Vehicle_Age_lt_1_Year,
                Vehicle_Age_gt_2_Years,
                Vehicle_Damage_Yes
                ):
        """
        Vehicle Data constructor
        Input: all features of the trained model for prediction
        """
        try:
            self.Gender = Gender
            self.Age = Age
            self.Driving_License = Driving_License
            self.Region_Code = Region_Code
            self.Previously_Insured = Previously_Insured
            self.Annual_Premium = Annual_Premium
            self.Policy_Sales_Channel = Policy_Sales_Channel
            self.Vintage = Vintage
            self.Vehicle_Age_lt_1_Year = Vehicle_Age_lt_1_Year
            self.Vehicle_Age_gt_2_Years = Vehicle_Age_gt_2_Years
            self.Vehicle_Damage_Yes = Vehicle_Damage_Yes

        except Exception as e:
            raise exceptions(e, sys) from e

    def get_vehicle_input_data_frame(self)-> DataFrame:
        """
        This function returns a DataFrame from  class input
        """
        try:
            
            vehicle_input_dict = self.get_vehicle_data_as_dict()
            df = DataFrame(vehicle_input_dict)

            # Apply the same lightweight custom transformations used during training
            # 1) Map Gender to binary if given as strings
            if 'Gender' in df.columns and df['Gender'].dtype == object:
                df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1})

            # 2) Drop identifier columns if present
            for col in ['id', '_id']:
                if col in df.columns:
                    df = df.drop(columns=[col])

            # 3) Create dummy variables for categorical features to match training pipeline
            cols_to_dummify = [c for c in ['Gender', 'Vehicle_Age', 'Vehicle_Damage'] if c in df.columns]
            if cols_to_dummify:
                df = pd.get_dummies(df, columns=cols_to_dummify, drop_first=True)

            # 4) Rename vehicle age dummy columns to match training names
            df = df.rename(columns={
                "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
                "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
            })

            # 5) Ensure integer type for boolean/dummy columns if present
            for col in ["Vehicle_Age_lt_1_Year", "Vehicle_Age_gt_2_Years", "Vehicle_Damage_Yes"]:
                if col in df.columns:
                    df[col] = df[col].astype('int')

            return df
        
        except Exception as e:
            raise exceptions(e, sys) from e


    def get_vehicle_data_as_dict(self):
        """
        This function returns a dictionary from VehicleData class input
        """
        logging.info("Entered get_usvisa_data_as_dict method as VehicleData class")

        try:
            input_data = {
                "Gender": [self.Gender],
                "Age": [self.Age],
                "Driving_License": [self.Driving_License],
                "Region_Code": [self.Region_Code],
                "Previously_Insured": [self.Previously_Insured],
                "Annual_Premium": [self.Annual_Premium],
                "Policy_Sales_Channel": [self.Policy_Sales_Channel],
                "Vintage": [self.Vintage],
                "Vehicle_Age_lt_1_Year": [self.Vehicle_Age_lt_1_Year],
                "Vehicle_Age_gt_2_Years": [self.Vehicle_Age_gt_2_Years],
                "Vehicle_Damage_Yes": [self.Vehicle_Damage_Yes]
            }

            logging.info("Created vehicle data dict")
            logging.info("Exited get_vehicle_data_as_dict method as VehicleData class")
            return input_data

        except Exception as e:
            raise exceptions(e, sys) from e

class VehicleDataClassifier:
    def __init__(self,prediction_pipeline_config: VehiclePredictorConfig = VehiclePredictorConfig(),) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction the value
        """
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise exceptions(e, sys)

    def predict(self, dataframe) -> str:
        """
        This is the method of VehicleDataClassifier
        Returns: Prediction in string format
        """
        try:
            logging.info("Entered predict method of VehicleDataClassifier class")
            model = Proj1Estimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result =  model.predict(dataframe)
            
            return result
        
        except Exception as e:
            raise exceptions(e, sys)