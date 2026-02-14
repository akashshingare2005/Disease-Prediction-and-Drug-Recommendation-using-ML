
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("api/dataset.csv")

X = df.drop("disease", axis=1)
y = df["disease"]

# Encode disease labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

print("🔥 Model trained successfully")

# Save everything
joblib.dump(model, "api/disease_model.pkl")
joblib.dump(le, "api/label_encoder.pkl")
joblib.dump(X.columns.tolist(), "api/symptoms.pkl")

print("✅ Model + encoder + symptoms saved")
