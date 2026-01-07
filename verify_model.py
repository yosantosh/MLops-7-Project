
import sys
import os
from src.entity.config_entity import XGBoostConfig
from src.entity.artifact_entity import DataTransformationArtifact
from src.components.model_trainer import ModelTrainer
from src.logger import logging

# Mock DataTransformationArtifact using existing files
artifact_dir = "Artifacts"
data_transformation_dir = os.path.join(artifact_dir, "data_transformation")
transformed_data_dir = os.path.join(data_transformation_dir, "transformed")
transformed_object_dir = os.path.join(data_transformation_dir, "transformed_object")

train_file = os.path.join(transformed_data_dir, "train.npy")
test_file = os.path.join(transformed_data_dir, "test.npy")
pre_obj_file = os.path.join(transformed_object_dir, "preprocessing.pkl")

print(f"Checking files:\n{train_file}\n{test_file}\n{pre_obj_file}")
if not os.path.exists(train_file):
    print("Train file missing!")
    sys.exit(1)
if not os.path.exists(test_file):
    print("Test file missing!")
    sys.exit(1)

dt_artifact = DataTransformationArtifact(
    transformed_train_file_path=train_file,
    transformed_test_file_path=test_file,
    transformed_object_file_path=pre_obj_file
)

# Initialize Config
config = XGBoostConfig()
print(f"Training XGBoost with: n_estimators={config.n_estimators}, max_depth={config.max_depth}")

# Train
trainer = ModelTrainer(
    data_transformation_artifact=dt_artifact,
    model_trainer_config=config
)

print("Starting training...")
try:
    artifact = trainer.initiate_model_trainer()
    print("Training complete.")
    print(f"F1 Score: {artifact.metric_artifact.f1_score}")
except Exception as e:
    print(f"Error: {e}")
    # Print stack trace if possible
    import traceback
    traceback.print_exc()
