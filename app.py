import os
import sys
import certifi
import pymongo
from uvicorn import run as app_run
from dotenv import load_dotenv
load_dotenv()
Mongo_DB_url=os.getenv("Mongodb_url")
ca=certifi.where()
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipeline1
from networksecurity.constant.Training_Pipeline import DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME
from networksecurity.utils.main_utils.utils import load_object


from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.utils.mlutils.model.estimator import NetworkModel
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")



client=pymongo.MongoClient(Mongo_DB_url,tlsCAFile=ca)
database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")
@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline1()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        print(df)

        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")

        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        print(df.iloc[0])
        print("Calling predict with shape:", df.shape)
        y_pred = network_model.predict(x=df)  # ✅ Should now wo

        df['predicted_column'] = y_pred
        df.to_csv('prediction_output/output.csv', index=False)

        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        print(f"Prediction error: {e}")
        return {"error": str(e)}
    
    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)