from networksecurity.entity.Arifacts_Entity import ClassificationMetricArtifact
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import precision_score,f1_score,recall_score

def get_classification_score(y_true,y_predicted)->ClassificationMetricArtifact:
    p_score=precision_score(y_true,y_predicted)
    recallscore=recall_score(y_true,y_predicted)
    f1score=f1_score(y_true,y_predicted)
    classification_metric=ClassificationMetricArtifact(f1_score=f1score,precision_score=p_score,recall_score=recallscore)
    return classification_metric


