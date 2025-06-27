import os
import pandas as pd
import numpy as np

TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"
TRAINING_FILE_PATH="train.csv"
TEST_FILE_PATH="test.csv"
PREPROCESSOR_MODEL="preprocessor.pkl"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")





DATA_INGESTION_DATABASE_NAME:str="Kanwal'sDatabase"
DATA_INGESTION_COLLECTION_NAME:str="NetworkSecurity"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.20


DATA_VALIDATION_DIR_NAME:str="Data_Validation"
DATA_VALIDATION_VALIDATED_DATA_DIR_NAME:str="Validated_Data"
DATA_VALIDATION_INVALID_DATA_DIR_NAME:str="Invalid_Data"
DATA_VALIDATION_DRIFT_REPORT_DIR_NAME:str="Drift_Report"
DATA_VALIDATION_DRIFT_REPORT_NAME:str="report.yaml"


DATA_TRANSFORMATION_DIR_NAME:str="Data_Transformation"
DATA_TRANSFORMED_DIR_NAME:str="transformed_data"
PREPROCESSOR_OBJECT_DIR_NAME:str="transformed_object"

KNN_IMPUTER_PARAMS:dict={
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":'uniform'


}



MODEL_TRAINER_DIR_NAME:str="model_trainer"
MODEL_TRAINED_NAME:str='model.pkl'
MODEL_EXPECTED_SCORE:float=0.60
MODEL_OVERFITTING_UNDERFITTING_THRESHOLD:float=0.5

TRAINING_BUCKET_NAME="kanwal0042"








