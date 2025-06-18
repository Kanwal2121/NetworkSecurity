import os
from datetime import datetime
from networksecurity.constant import Training_Pipeline

print(Training_Pipeline.ARTIFACT_DIR)

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.artifacs_dir_name=Training_Pipeline.ARTIFACT_DIR
        self.pipeline_name=Training_Pipeline.PIPELINE_NAME
        self.artifacts_dir=os.path.join(self.artifacs_dir_name,timestamp)

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(training_pipeline_config.artifacts_dir,Training_Pipeline.DATA_INGESTION_DIR_NAME)
        self.raw_file_path:str=os.path.join(self.data_ingestion_dir,Training_Pipeline.DATA_INGESTION_FEATURE_STORE_DIR,Training_Pipeline.FILE_NAME)
        self.training_file_path:str=os.path.join(self.data_ingestion_dir,Training_Pipeline.DATA_INGESTION_INGESTED_DIR,Training_Pipeline.TRAINING_FILE_PATH)
        self.test_file_path:str=os.path.join(self.data_ingestion_dir,Training_Pipeline.DATA_INGESTION_INGESTED_DIR,Training_Pipeline.TEST_FILE_PATH)
        self.database_name:str=Training_Pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name:str=Training_Pipeline.DATA_INGESTION_COLLECTION_NAME
        self.train_test_split_ratio:float=Training_Pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO



