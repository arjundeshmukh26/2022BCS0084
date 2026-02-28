from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

NAME = "Gaurav Nanasaheb Malave"
ROLL_NO = "2022BCD0017"

app = FastAPI(title="Wine Quality Prediction API")

with open('model/wine_model.pkl', 'rb') as f:
    model = pickle.load(f)

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
def read_root():
    return {
        "message": "Wine Quality Prediction API",
        "name": NAME,
        "roll_no": ROLL_NO
    }

@app.post("/predict")
def predict(features: WineFeatures):
    input_data = np.array([[
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
    
    prediction = model.predict(input_data)[0]
    
    return {
        "name": NAME,
        "roll_no": ROLL_NO,
        "wine_quality": round(prediction)
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}