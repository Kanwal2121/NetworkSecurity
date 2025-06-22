from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    columns_status:bool
    data_drift_status:bool
    valid_train_path:str
    valid_test_path:str
    invalid_train_path:str
    invalid_test_path:str
    drift_report_file_path:str

@dataclass
class DataTransformationArtifacts:
    transformed_train_file_path:str
    transformed_test_file_path:str
    preprocessor_file_path:str
    

