import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load student dataset
df = pd.read_csv("data/students.csv")

# Create academic risk categories
def identify_risk(row):

    if row["Attendance"] < 60 or row["Average"] < 40:
        return "High Risk"

    elif row["Attendance"] < 75 or row["Average"] < 60:
        return "Moderate Risk"

    else:
        return "Low Risk"

df["Risk_Level"] = df.apply(identify_risk, axis=1)

# Select input features
features = [
    "Attendance",
    "Average",
    "Mathematics",
    "English",
    "Science",
    "Computer",
    "Social_Studies"
]

X = df[features]
y = df["Risk_Level"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Train Random Forest Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Training Completed!")
print("Model Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Save model
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/performance_model.pkl")

print("\nModel saved successfully!")