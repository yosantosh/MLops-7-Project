import sys

import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from src.exception import exceptions
from src.logger import logging

class TargetValueMapping:
    def __init__(self):
        self.yes:int = 0
        self.no:int = 1
    def _asdict(self):
        return self.__dict__
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(),mapping_response.keys()))

class MyModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        :param preprocessing_object: Input Object of preprocesser
        :param trained_model_object: Input Object of trained model 
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: pd.DataFrame) -> DataFrame:
        """
        Function accepts preprocessed inputs (with all custom transformations already applied),
        applies scaling using preprocessing_object, and performs prediction on transformed features.
        """
        try:
            logging.info("Starting prediction process.")

            # Step 1: Apply scaling transformations using the pre-trained preprocessing object
            try:
                transformed_feature = self.preprocessing_object.transform(dataframe)
            except ValueError as ve:
                # Handle missing columns error by adding the missing columns with default values
                msg = str(ve)
                if "columns are missing" in msg:
                    # extract set-like content: { 'col1', 'col2' }
                    import re
                    m = re.search(r"\{(.+)\}", msg)
                    if m:
                        cols = [c.strip().strip("'\" ") for c in m.group(1).split(',')]
                        for c in cols:
                            if c and c not in dataframe.columns:
                                dataframe[c] = 0
                        transformed_feature = self.preprocessing_object.transform(dataframe)
                    else:
                        raise
                else:
                    raise

            # Step 2: Perform prediction using the trained model
            logging.info("Using the trained model to get predictions")
            predictions = self.trained_model_object.predict(transformed_feature)

            return predictions

        except Exception as e:
            logging.error("Error occurred in predict method", exc_info=True)
            raise exceptions(e, sys) from e


    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"