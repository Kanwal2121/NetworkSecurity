import os
import sys
import numpy as np
import pickle

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant import Training_Pipeline
from networksecurity.logging.logger import logging
import dill
import yaml
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


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
    

def load_object(filepath:str)->object:
    try:
      with open(filepath,"rb") as file_object:
           return  pickle.load(file_object)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array(filepath:str)->np.array:
    try:
      with open(filepath,"rb") as file_object:
           return  np.load(file_object)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def evaluate_models(X_train:np.array,X_test:np.array,y_train:np.array,y_test:np.array,models:dict)->dict:
    report:dict={}
    b_params:dict={}
    for i in range(len(list(models))):
        model=list(models.values())[i]
        #bestparam=params[list(models.keys())[i]]

        #gs=GridSearchCV(model,bestparam,cv=5)
        #gs.fit(X_train,y_train)
        #model.set_params(**gs.best_params_)
        model.fit(X_train,y_train)

        

        predicted_values=model.predict(X_test)

        Score=r2_score(y_test,predicted_values)

        report[list(models.keys())[i]]=Score
        #b_params[list(models.keys())[i]]=gs.best_params_


    return report 
    


    

