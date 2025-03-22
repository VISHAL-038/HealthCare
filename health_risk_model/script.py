import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from faker import Faker
from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# Initialize Faker
fake = Faker()

# Number of samples
data_size = 10000

# Generate synthetic data
np.random.seed(42)

age = np.random.randint(18, 80, data_size)
bmi = np.random.uniform(15, 40, data_size).round(1)
bp = np.random.randint(80, 180, data_size)
heart_rate = np.random.randint(50, 120, data_size)
blood_sugar = np.random.randint(70, 200, data_size)
cholesterol = np.random.randint(100, 300, data_size)

# Define health condition based on thresholds
def classify_health(bmi, bp, heart_rate, blood_sugar, cholesterol):
    if bmi < 25 and bp < 120 and heart_rate < 80 and blood_sugar < 100 and cholesterol < 200:
        return "Healthy"
    elif bmi < 30 and bp < 140 and heart_rate < 90 and blood_sugar < 130 and cholesterol < 250:
        return "At Risk"
    else:
        return "High Risk"

# Define specific health risks
def determine_health_risk(bmi, bp, heart_rate, blood_sugar, cholesterol, health_status):
    risks = []
    if bmi >= 30:
        risks.append("Obesity")
    elif 25 <= bmi < 30:
        risks.append("Overweight")
    if bp >= 140:
        risks.append("Hypertension")
    elif 120 <= bp < 140:
        risks.append("Pre-Hypertension")
    if blood_sugar >= 130:
        risks.append("Diabetes")
    elif 100 <= blood_sugar < 130:
        risks.append("Pre-Diabetes")
    if cholesterol >= 250:
        risks.append("Heart Disease")
    elif 200 <= cholesterol < 250:
        risks.append("Elevated Cholesterol")
    if heart_rate >= 100:
        risks.append("Tachycardia (High Heart Rate)")
    elif heart_rate <= 50:
        risks.append("Bradycardia (Low Heart Rate)")
    
    # Ensure 'At Risk' and 'High Risk' always have a mapped condition
    if health_status in ["At Risk", "High Risk"] and not risks:
        risks.append("General Health Risk - Further Evaluation Recommended")
    
    if not risks:
        return "No Risk"
    return ", ".join(risks)

health_condition = [classify_health(bmi[i], bp[i], heart_rate[i], blood_sugar[i], cholesterol[i]) for i in range(data_size)]
health_risk = [determine_health_risk(bmi[i], bp[i], heart_rate[i], blood_sugar[i], cholesterol[i], health_condition[i]) for i in range(data_size)]

# Create DataFrame
df = pd.DataFrame({
    'Age': age,
    'BMI': bmi,
    'Blood Pressure': bp,
    'Heart Rate': heart_rate,
    'Blood Sugar': blood_sugar,
    'Cholesterol': cholesterol,
    'Health Condition': health_condition,
    'Health Risk': health_risk
})

# Encode target variable
label_encoder = LabelEncoder()
df['Health Condition'] = label_encoder.fit_transform(df['Health Condition'])

# Select features and target
X = df[['Age', 'BMI', 'Blood Pressure', 'Heart Rate', 'Blood Sugar', 'Cholesterol']]
y = df['Health Condition']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train RandomForestClassifier model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
with open("health_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Load the model
with open("health_model.pkl", "rb") as file:
    loaded_model = pickle.load(file)

# Flask API
app = Flask(__name__)

@app.route('/')
def home():
    return "Health Prediction API is running!"

@app.route('/predict_health', methods=['POST'])
def predict_health():
    data = request.json

    # Ensure input is formatted correctly
    input_df = pd.DataFrame([data], columns=['Age', 'BMI', 'Blood Pressure', 'Heart Rate', 'Blood Sugar', 'Cholesterol'])

    # Make a prediction
    prediction = loaded_model.predict(input_df)[0]  # Ensure proper input format
    health_status = label_encoder.inverse_transform([prediction])[0]

    # Determine health risk
    health_risk = determine_health_risk(data['BMI'], data['Blood Pressure'], data['Heart Rate'], data['Blood Sugar'], data['Cholesterol'], health_status)

    return jsonify({
        'Predicted Health Condition': health_status,
        'Health Risk': health_risk
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
