from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logging.logger import logging



if __name__=="__main__":
    trainingpipelineconfig=TrainingPipelineConfig()
    data_ingestion_config=DataIngestionConfig(trainingpipelineconfig)
    obj=DataIngestion(data_ingestion_config=data_ingestion_config)
    
    logging.info("Initiate data ingestion")

    dataingestionartifact=obj.initiate_data_ingestion()
    print(dataingestionartifact)