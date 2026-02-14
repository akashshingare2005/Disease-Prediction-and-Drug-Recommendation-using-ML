
import joblib
import numpy as np

model = joblib.load("api/disease_model.pkl")
label_encoder = joblib.load("api/label_encoder.pkl")
symptom_list = joblib.load("api/symptoms.pkl")

def predict_disease(symptoms_text):
    symptoms = [s.strip().lower() for s in symptoms_text.split(",")]

    input_vector = [
        1 if symptom in symptoms else 0
        for symptom in symptom_list
    ]

    input_array = np.array(input_vector).reshape(1, -1)

    prediction_encoded = model.predict(input_array)[0]
    probs = model.predict_proba(input_array)[0]

    disease = label_encoder.inverse_transform([prediction_encoded])[0]
    probability = round(max(probs) * 100, 2)

    return disease, probability
