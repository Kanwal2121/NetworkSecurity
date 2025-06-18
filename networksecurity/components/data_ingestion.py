import os
import sys
import pandas as pd
import pymongo
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.DataIngestionArtifacts import DataIngestionArtifact
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

Mongodb_url=os.getenv("Mongodb_url")





class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_dataframe(self):
        try:
            logging.info("Data extractation  from pymongo Database started ")
            self.database_name=self.data_ingestion_config.database_name
            self.collection_name=self.data_ingestion_config.collection_name
            self.pymongo_client=pymongo.MongoClient(Mongodb_url)
            collection=self.pymongo_client[self.database_name][self.collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            df.replace({"na":np.nan},inplace=True)
            logging.info("Data extraction completed")
            return df
        
        
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_feature_store(self,Dataframe:pd.DataFrame):
        try:
            logging.info("Storing raw data csv into feature store")
            self.raw_file_path=self.data_ingestion_config.raw_file_path
            data_file_path=os.path.dirname(self.raw_file_path)
            os.makedirs(data_file_path,exist_ok=True)
            Dataframe.to_csv(self.raw_file_path,index=False,header=True)
            logging.info("raw csv stored")

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def perform_train_test_split(self,Dataframe:pd.DataFrame):
        try:
            logging.info("Train Test Split Started")
            Train_data,Test_data=train_test_split(Dataframe,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)
            self.train_file_path=self.data_ingestion_config.training_file_path
            file_path=os.path.dirname(self.train_file_path)
            os.makedirs(file_path,exist_ok=True)

            self.test_file_path=self.data_ingestion_config.test_file_path
            Train_data.to_csv(self.train_file_path,index=False,header=True)
            Test_data.to_csv(self.test_file_path,index=False,header=True)
            logging.info("Train Test Split Completed")
            return Dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)



        

    def initiate_data_ingestion(self):
        try:
            Dataset=self.get_dataframe()
            self.export_data_into_feature_store(Dataframe=Dataset)
            self.perform_train_test_split(Dataframe=Dataset)
            dataingestionartifact=DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.test_file_path)
            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)





        



        

        



        
