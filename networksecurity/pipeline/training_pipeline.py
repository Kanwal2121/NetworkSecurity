from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig,TrainingPipelineConfig
from networksecurity.entity.Arifacts_Entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifacts,ModelTrainerArtifact
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.cloud.s3_syncer import S3Sync

from networksecurity.constant.Training_Pipeline import TRAINING_BUCKET_NAME
import sys



class TrainingPipeline1:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        self.s3_sync = S3Sync()

    def start_data_ingestion(self):
        try:
            data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifacts:DataIngestionArtifact):
        try:
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifats=data_ingestion_artifacts,data_validation_config=data_validation_config)
            data_validation_artifacts=data_validation.initiate_data_validation()
            return data_validation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_trasnformation(self,data_validation_artifacts:DataValidationArtifact):
        try:
            data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation=DataTransformation(data_validation_artifacts=data_validation_artifacts,data_transformation_config=data_transformation_config)
            data_transformation_artifacts=data_transformation.initiate_data_transformation()
            return data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_training(self,data_transformation_artifacts:DataTransformationArtifacts):
        try:
            model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_transformation=ModelTrainer(data_transformation_artifacts=data_transformation_artifacts,modeltrainer_config=model_trainer_config)
            model_transformation_artifacts=model_transformation.initiate_model_trainer()
            return model_transformation_artifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

        
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifacts_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
        
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        
    def run_pipeline(self):
        try:
            logging.info("start")
            data_ingestion_artifacts=self.start_data_ingestion()
            data_validation_artifacts=self.start_data_validation(data_ingestion_artifacts=data_ingestion_artifacts)
            data_transformation_artifats=self.start_data_trasnformation(data_validation_artifacts=data_validation_artifacts)
            model_trainer_artifacts=self.start_model_training(data_transformation_artifacts=data_transformation_artifats)
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()

        except Exception as e:
            raise NetworkSecurityException(e,sys)



    

        




