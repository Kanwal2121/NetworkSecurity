import os
import sys
import json
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import certifi
import pymongo
import pymongo.mongo_client
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


load_dotenv()
Mongodb_url=os.getenv("Mongodb_url")

ca=certifi.where()

class NetworkDataExtract:
    def __init__(self):
        pass
    def csv_to_json_converter(self,Filepath):
        try:
            Dataset=pd.read_csv(Filepath)
            Dataset.reset_index(drop=True,inplace=True)
            Records=list(json.loads(Dataset.T.to_json()).values())
            return Records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.records=records
            self.database=database
            self.collection=collection
            self.Mongodb_client=pymongo.MongoClient(Mongodb_url)
            self.database=self.Mongodb_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)




        except Exception as e:
            raise NetworkSecurityException(e,sys) 


if __name__=="__main__":
    File_Path="Network_data/phisingData.csv"
    Database="Kanwal'sDatabase"
    Collection="NetworkSecurity"
    network_data_obj=NetworkDataExtract()
    records=network_data_obj.csv_to_json_converter(Filepath=File_Path)
    print(records)
    length=network_data_obj.insert_data_to_mongodb(records=records,database=Database,collection=Collection)
    print(length)






