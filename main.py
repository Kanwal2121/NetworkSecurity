from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.logging.logger import logging



if __name__=="__main__":
    trainingpipelineconfig=TrainingPipelineConfig()
    data_ingestion_config=DataIngestionConfig(trainingpipelineconfig)
    obj=DataIngestion(data_ingestion_config=data_ingestion_config)
    
    logging.info("Initiate data ingestion")

    dataingestionartifact=obj.initiate_data_ingestion()
    print(dataingestionartifact)
    



    datavalidationconfig=DataValidationConfig(trainingpipelineconfig)
    object=DataValidation(data_ingestion_artifats=dataingestionartifact,data_validation_config=datavalidationconfig)
    data_validation_artifacts=object.initiate_data_validation()
    #print(r)


    datatransformationconfig=DataTransformationConfig(trainingpipelineconfig)
    data_transformation_object=DataTransformation(data_validation_artifacts=data_validation_artifacts,data_transformation_config=datatransformationconfig)
    data_transformation_artifacts=data_transformation_object.initiate_data_transformation()
    print(data_transformation_artifacts)

    model_train_config=ModelTrainerConfig(trainingpipelineconfig)
    modeltrainobject=ModelTrainer(data_transformation_artifacts,model_train_config)
    model_trainer_artifacts=modeltrainobject.initiate_model_trainer()
    print(model_trainer_artifacts)








