from networksecurity.entity.Arifacts_Entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant import Training_Pipeline
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import read_schema_yaml,write_yaml
import sys
from scipy.stats import ks_2samp
import pandas as pd
import os



class DataValidation:
    def __init__(self,data_ingestion_artifats:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        self.data_vaidation_config=data_validation_config
        self.data_ingestion_artifacts=data_ingestion_artifats
        self.schema_config=read_schema_yaml(Training_Pipeline.SCHEMA_FILE_PATH)

    @staticmethod
    def read_data(filepath)->pd.DataFrame:
        
        return pd.read_csv(filepath)
    
    def validate_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            logging.info("No of Column Checking")
            number_of_columns=len(self.schema_config['columns'])
            logging.info(f"Number of columns{number_of_columns}")
            if(number_of_columns==len(dataframe.columns)):
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_data_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            logging.info("detect data drift")
            Status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                sample_distribution=ks_2samp(d1,d2)
                if threshold<=sample_distribution.pvalue:
                    is_found=False
                else:
                    is_found=True
                    Status=False
                report.update({column:{"p_value":float(sample_distribution.pvalue),
                                       "drift_status":is_found}})
            
            drift_report_filepath=os.path.dirname(self.data_vaidation_config.drift_report_file_path)
            os.makedirs(drift_report_filepath,exist_ok=True)
            write_yaml(file_path=self.data_vaidation_config.drift_report_file_path,content=report)
            return is_found


        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_path=self.data_ingestion_artifacts.train_file_path
            test_path=self.data_ingestion_artifacts.test_file_path
            train_dataframe=DataValidation.read_data(train_path)
            test_dataframe=DataValidation.read_data(test_path)


            status=self.validate_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"Train Data not contain all the columns. \n"
            status=self.validate_columns(dataframe=test_dataframe)
            if not status:
                error_message=f"Test Data not contain all the columns. \n"


            status1=self.detect_data_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_vaidation_config.valid_training_data)
            os.makedirs(dir_path,exist_ok=True)
            train_dataframe.to_csv(self.data_vaidation_config.valid_training_data,index=False,header=True)
            test_dataframe.to_csv(self.data_vaidation_config.valid_test_data,index=False,header=True)
            data_validation_artifacts=DataValidationArtifact(
                columns_status=status,
                data_drift_status=status1,
                valid_train_path=self.data_vaidation_config.valid_training_data,
                valid_test_path=self.data_vaidation_config.valid_test_data,
                invalid_train_path=None,
                invalid_test_path=None,
                drift_report_file_path=self.data_vaidation_config.drift_report_file_path
            )
            return data_validation_artifacts



        except Exception as e:
            raise NetworkSecurityException(e,sys)

    



        