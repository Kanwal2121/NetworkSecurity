import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.Arifacts_Entity import DataTransformationArtifacts,ModelTrainerArtifact
from networksecurity.utils.mlutils.metric.clasifiaction_metric import get_classification_score
from networksecurity.utils.mlutils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_preprocessor_object,load_object,load_numpy_array,evaluate_models
import mlflow


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
import dagshub
dagshub.init(repo_owner='Kanwal2121', repo_name='NetworkSecurity', mlflow=True)




class ModelTrainer:
    def __init__(self,data_transformation_artifacts:DataTransformationArtifacts,modeltrainer_config:ModelTrainerConfig):
        self.data_transformation_artifacts=data_transformation_artifacts
        self.modeltrainer_config=modeltrainer_config
    def track_mlflow(self, best_model, classifiactiommetric):
        with mlflow.start_run():
            metrics = {
                "f1_score": classifiactiommetric.f1_score,
                "precision_score": classifiactiommetric.precision_score,
                "recall_score": classifiactiommetric.recall_score
            }

            mlflow.log_metrics(metrics)
            #mlflow.sklearn.log_model(best_model,name="model")







       

    


    def initiate_model_trainer(self):
        try:
       
            train_array=load_numpy_array(filepath=self.data_transformation_artifacts.transformed_train_file_path)
            
            test_array=load_numpy_array(filepath=self.data_transformation_artifacts.transformed_test_file_path)
            

            models={
                "LogisticRegression":LogisticRegression(),
                "KNeighborsClassifier":KNeighborsClassifier(),
                "DecisionTreeClassifier":DecisionTreeClassifier(),
                "AdaBoostClassifier":AdaBoostClassifier(),
                "GradientBoostingClassifier":GradientBoostingClassifier(),
                "RandomForestClassifier":RandomForestClassifier()




            }
            '''
            best_params ={
            "DecisionTreeClassifier": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "RandomForestClassifier":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "GradientBoostingClassifier":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "LogisticRegression":{},
            "AdaBoostClassifier":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
        '''
            



            X_train,X_test,y_train,y_test=(train_array[:,:-1],test_array[:,:-1],train_array[:,-1],test_array[:,-1])

            report=evaluate_models(X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test,models=models)

            best_model_score=max(report.values())
            for key,value in report.items():
                if value==best_model_score:
                    best_model_name=key
            #for key,value in b_params.items():
                #if key==best_model_name:
                    #param=value

            best_model=models[best_model_name]
            #best_model.set_params(**param)
            logging.info(f"{best_model}")

            best_model.fit(X_train,y_train)
            y_pred_train=best_model.predict(X_train)
            Classification_Metric_Train=get_classification_score(y_true=y_train,y_predicted=y_pred_train)
            y_pred_test=best_model.predict(X_test)
            Classification_Metric_Test=get_classification_score(y_true=y_test,y_predicted=y_pred_test)
            logging.info(f"{Classification_Metric_Test}")
            self.track_mlflow(best_model=best_model,classifiactiommetric=Classification_Metric_Test)

            model_dir=os.path.dirname(self.modeltrainer_config.trained_model_file_path)
            os.makedirs(model_dir,exist_ok=True)

            preprocessor=load_object(self.data_transformation_artifacts.preprocessor_file_path)

            Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
            save_preprocessor_object(filepath=self.modeltrainer_config.trained_model_file_path,object=NetworkModel)
            save_preprocessor_object("final_model/model.pkl",best_model)

            model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.modeltrainer_config.trained_model_file_path,
                                                        train_metric_artifact=Classification_Metric_Train,
                                                        test_metric_artifact=Classification_Metric_Test
                                                        
                                                        

            )
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)














    
