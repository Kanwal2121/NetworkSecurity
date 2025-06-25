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

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str=os.path.join(training_pipeline_config.artifacts_dir,Training_Pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir:str=os.path.join(self.data_validation_dir,Training_Pipeline.DATA_VALIDATION_VALIDATED_DATA_DIR_NAME)
        self.valid_training_data:str=os.path.join(self.valid_data_dir,Training_Pipeline.TRAINING_FILE_PATH)
        self.valid_test_data:str=os.path.join(self.valid_data_dir,Training_Pipeline.TEST_FILE_PATH)

        self.invalid_data_dir:str=os.path.join(self.data_validation_dir,Training_Pipeline.DATA_VALIDATION_INVALID_DATA_DIR_NAME)
        self.invalid_training_data:str=os.path.join(self.invalid_data_dir,Training_Pipeline.TRAINING_FILE_PATH)
        self.invalid_test_data:str=os.path.join(self.invalid_data_dir,Training_Pipeline.TEST_FILE_PATH)

        self.driftreport_dir:str=os.path.join(self.data_validation_dir,Training_Pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR_NAME)
        self.drift_report_file_path:str=os.path.join(self.driftreport_dir,Training_Pipeline.DATA_VALIDATION_DRIFT_REPORT_NAME)






class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir:str=os.path.join(training_pipeline_config.artifacts_dir,Training_Pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_data_dir:str=os.path.join(self.data_transformation_dir,Training_Pipeline.DATA_TRANSFORMED_DIR_NAME)
        self.preprocessor_dir:str=os.path.join(self.data_transformation_dir,Training_Pipeline.PREPROCESSOR_OBJECT_DIR_NAME)
        self.transformned_train_file_path:str=os.path.join(self.transformed_data_dir,Training_Pipeline.TRAINING_FILE_PATH.replace("csv","npy"))
        self.transformned_test_file_path:str=os.path.join(self.transformed_data_dir,Training_Pipeline.TEST_FILE_PATH.replace("csv","npy"))
        
        self.preprocessor_file_path:str=os.path.join(self.preprocessor_dir,Training_Pipeline.PREPROCESSOR_MODEL)

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.trained_model_dir_name:str=os.path.join(training_pipeline_config.artifacts_dir,Training_Pipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path:str=os.path.join(self.trained_model_dir_name,Training_Pipeline.MODEL_TRAINED_NAME)
        self.model_expected_score:float=Training_Pipeline.MODEL_EXPECTED_SCORE
        self.model_underfitting_overfitting_threshold:float=Training_Pipeline.MODEL_OVERFITTING_UNDERFITTING_THRESHOLD
        


        