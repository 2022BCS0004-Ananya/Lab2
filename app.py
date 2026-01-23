from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="Wine Quality Inference API")

# Load trained model
MODEL_PATH = os.path.join("model", "model.joblib")
model = joblib.load(MODEL_PATH)


# -------- Input Schema (for POST) --------
class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float


@app.get("/")
def root():
    return {"message": "Wine Quality Prediction API running"}


# -------- POST /predict --------
@app.post("/predict")
def predict_post(features: WineFeatures):
    data = np.array([[ 
        features.fixed_acidity,
        features.volatile_acidity,
        features.citric_acid,
        features.residual_sugar,
        features.chlorides,
        features.free_sulfur_dioxide,
        features.total_sulfur_dioxide,
        features.density,
        features.pH,
        features.sulphates,
        features.alcohol
    ]])

    prediction = model.predict(data)

    return {"predicted_quality": float(prediction[0])}


# -------- GET /predict --------
@app.get("/predict")
def predict_get(
    fixed_acidity: float,
    volatile_acidity: float,
    citric_acid: float,
    residual_sugar: float,
    chlorides: float,
    free_sulfur_dioxide: float,
    total_sulfur_dioxide: float,
    density: float,
    pH: float,
    sulphates: float,
    alcohol: float
):
    data = np.array([[ 
        fixed_acidity,
        volatile_acidity,
        citric_acid,
        residual_sugar,
        chlorides,
        free_sulfur_dioxide,
        total_sulfur_dioxide,
        density,
        pH,
        sulphates,
        alcohol
    ]])

    prediction = model.predict(data)

    return {"predicted_quality": float(prediction[0])}
