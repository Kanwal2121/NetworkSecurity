import os
import sys
import numpy as np
import pandas as pd
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.Arifacts_Entity import DataValidationArtifact,DataTransformationArtifacts
from networksecurity.utils.main_utils.utils import save_array,save_preprocessor_object
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.Training_Pipeline import TARGET_COLUMN,KNN_IMPUTER_PARAMS
from sklearn.impute import KNNImputer
from sklearn.pipeline  import Pipeline



class DataTransformation:
    def __init__(self,data_validation_artifacts:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        self.data_validation_arifacts=data_validation_artifacts
        self.da_transformantion_config=data_transformation_config

    @staticmethod
    def read_data(filepath:str)->pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def create_preprocessor(cls)->Pipeline:
        try:
            imputer:KNNImputer=KNNImputer(**KNN_IMPUTER_PARAMS)
            preprocessor:Pipeline=Pipeline(steps=[("imputer",imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        


    def initiate_data_transformation(self):
        try:
            logging.info("Reading Of  Valiadted data started")
            #self.validated_train_file_path=self.data_validation_arifacts.valid_train_path
            #self.validated_test_file_path=self.data_validation_arifacts.valid_test_path
            train_dataframe=DataTransformation.read_data(self.data_validation_arifacts.valid_train_path)
            test_dataframe=DataTransformation.read_data(self.data_validation_arifacts.valid_test_path)
            logging.info("Reading Of  Valiadted data Completed")

            input_train_data=train_dataframe.drop(columns=[TARGET_COLUMN],axis=1)
            output_train_data=train_dataframe[TARGET_COLUMN]
            output_train_data=output_train_data.replace(-1,0)
            

            input_test_data=test_dataframe.drop(columns=[TARGET_COLUMN],axis=1)
            output_test_data=test_dataframe[TARGET_COLUMN]
            output_test_data=output_test_data.replace(-1,0)
            

            preprocessor=self.create_preprocessor()

            train_transformed_data=preprocessor.fit_transform(input_train_data)
            test_transformed_data=preprocessor.transform(input_test_data)

            train_arr=np.c_[train_transformed_data,np.array(output_train_data)]
            test_arr=np.c_[test_transformed_data,np.array(output_test_data)]

            save_array(filepath=self.da_transformantion_config.transformned_train_file_path,array=train_arr)
            save_array(filepath=self.da_transformantion_config.transformned_test_file_path,array=test_arr)
            save_preprocessor_object(filepath=self.da_transformantion_config.preprocessor_file_path,object=preprocessor)


            datatransformationartifact=DataTransformationArtifacts(
                transformed_train_file_path=self.da_transformantion_config.transformned_train_file_path,
                transformed_test_file_path=self.da_transformantion_config.transformned_test_file_path,
                preprocessor_file_path=self.da_transformantion_config.preprocessor_file_path





            )
            return datatransformationartifact



            





        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

        
