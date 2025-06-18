import os
import pandas as pd

TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"
TRAINING_FILE_PATH="train.csv"
TEST_FILE_PATH="test.csv"






DATA_INGESTION_DATABASE_NAME:str="Kanwal'sDatabase"
DATA_INGESTION_COLLECTION_NAME:str="NetworkSecurity"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.20

