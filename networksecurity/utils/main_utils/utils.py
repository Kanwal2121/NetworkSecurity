import os
import sys
import numpy as np
import pickle

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant import Training_Pipeline
from networksecurity.logging.logger import logging
import dill
import yaml


def read_schema_yaml(File_path:str)->dict:
    try:
        with open(File_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def write_yaml(file_path:str,content:object)->None:
    try:
            
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_array(filepath:str,array:np.array):
    try:
        file_dir=os.path.dirname(filepath)
        os.makedirs(file_dir,exist_ok=True)
        with open(filepath,"wb") as file:
            np.save(file,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
            

def save_preprocessor_object(filepath:str,object:object):
    try:
        file_dir=os.path.dirname(filepath)
        os.makedirs(file_dir,exist_ok=True)
        with open(filepath,"wb") as file:
            pickle.dump(object,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)       