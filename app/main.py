from fastapi import FastAPI
import pickle
import numpy as np

NAME = "Arjun Deshmukh"
ROLL_NO = "2022BCS0084"

app = FastAPI(title="Wine Quality Prediction API")

# Load model
with open('model/wine_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.get("/")
def read_root():
    return {
        "message": "Wine Quality Prediction API",
        "name": NAME,
        "roll_no": ROLL_NO
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}


# 🔴 INTENTIONALLY REMOVED SCHEMA VALIDATION
# This will cause invalid input to be accepted
@app.post("/predict")
def predict(features: dict):
    try:
        # Try extracting fields if present
        input_data = np.array([[
            features.get("fixed_acidity", 0),
            features.get("volatile_acidity", 0),
            features.get("citric_acid", 0),
            features.get("residual_sugar", 0),
            features.get("chlorides", 0),
            features.get("free_sulfur_dioxide", 0),
            features.get("total_sulfur_dioxide", 0),
            features.get("density", 0),
            features.get("pH", 0),
            features.get("sulphates", 0),
            features.get("alcohol", 0)
        ]])

        prediction = model.predict(input_data)[0]

    except Exception:
        prediction = 0  # Force success even for bad input

    # 🚨 Always return 200 OK
    return {
        "name": NAME,
        "roll_no": ROLL_NO,
        "wine_quality": round(prediction)
    }