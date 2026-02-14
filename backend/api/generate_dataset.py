
import pandas as pd
import random

# Master Symptom List (40 symptoms)
symptoms = [
    "fever","cough","cold","headache","fatigue","nausea","vomiting","diarrhea",
    "chest_pain","shortness_of_breath","sore_throat","runny_nose","sneezing",
    "body_pain","joint_pain","muscle_pain","dizziness","loss_of_appetite",
    "weight_loss","weight_gain","blurred_vision","abdominal_pain",
    "constipation","back_pain","skin_rash","itching","frequent_urination",
    "burning_urination","excessive_thirst","night_sweats",
    "anxiety","depression","insomnia","palpitations",
    "high_bp","low_bp","dry_cough","wet_cough","wheezing",
    "loss_of_smell","loss_of_taste"
]

# 30 Diseases with Core Symptom Patterns
disease_map = {
    "Flu": ["fever","cough","body_pain","fatigue","sore_throat"],
    "Common Cold": ["cold","cough","runny_nose","sneezing"],
    "Migraine": ["headache","nausea","dizziness"],
    "Diabetes": ["excessive_thirst","frequent_urination","weight_loss"],
    "Hypertension": ["high_bp","headache","dizziness"],
    "Hypotension": ["low_bp","fatigue","dizziness"],
    "Asthma": ["shortness_of_breath","wheezing","dry_cough"],
    "Pneumonia": ["fever","chest_pain","wet_cough"],
    "COVID-19": ["fever","dry_cough","loss_of_smell","fatigue"],
    "Tuberculosis": ["weight_loss","night_sweats","wet_cough"],
    "Food Poisoning": ["vomiting","diarrhea","abdominal_pain"],
    "Gastritis": ["abdominal_pain","nausea","constipation"],
    "Depression": ["depression","fatigue","insomnia"],
    "Anxiety Disorder": ["anxiety","palpitations","insomnia"],
    "Arthritis": ["joint_pain","fatigue","back_pain"],
    "Malaria": ["fever","chills","fatigue"],
    "Dengue": ["fever","body_pain","skin_rash"],
    "Chickenpox": ["fever","skin_rash","fatigue"],
    "Typhoid": ["fever","abdominal_pain","fatigue"],
    "Bronchitis": ["wet_cough","fatigue","chest_pain"],
    "Heart Attack": ["chest_pain","shortness_of_breath","palpitations"],
    "Stroke": ["dizziness","weakness","blurred_vision"],
    "Allergy": ["sneezing","itching","runny_nose"],
    "Kidney Infection": ["burning_urination","fever","back_pain"],
    "Liver Disease": ["weight_loss","fatigue","abdominal_pain"],
    "Obesity": ["weight_gain","fatigue"],
    "Thyroid Disorder": ["weight_change","fatigue","anxiety"],
    "Sinusitis": ["headache","runny_nose","sneezing"],
    "Anemia": ["fatigue","dizziness","palpitations"],
    "Eczema": ["skin_rash","itching"]
}

data = []

# Generate 50 records per disease
for disease, core_symptoms in disease_map.items():
    for _ in range(50):
        row = {}

        for symptom in symptoms:
            if symptom in core_symptoms:
                row[symptom] = 1
            else:
                # Small random noise
                row[symptom] = random.choices([0,1], weights=[0.9,0.1])[0]

        row["disease"] = disease
        data.append(row)

df = pd.DataFrame(data)
df.to_csv("api/dataset.csv", index=False)

print("✅ Structured dataset generated successfully")
print("Total records:", len(df))
print("Total diseases:", df['disease'].nunique())

