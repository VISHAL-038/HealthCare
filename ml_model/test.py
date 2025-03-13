import requests
import json

# Flask API URL
url = "http://127.0.0.1:5000/predict"

# List of test cases
test_cases = [
    {"symptoms": "Cough,High Fever,Runny Nose,Headache,Sneezing,Weakness,Body Pain"},
    {"symptoms": "Vomiting,Stomach Pain,Diarrhoea,Dehydration,Nausea,Loss of Appetite"},
    {"symptoms": "Fever,Cough,Breathlessness,Loss of Smell,Fatigue,Body Ache,Headache"},
    {"symptoms": "Weight Loss,Excessive Hunger,Polyuria,Blurred Vision,Fatigue,Family History"},
    {"symptoms": "Chest Pain,Fast Heart Rate,Palpitations,Weakness,Shortness of Breath"},
    {"symptoms": "Yellowing of Eyes,Dark Urine,Abdominal Pain,Loss of Appetite,Mild Fever"},
    {"symptoms": "Burning Micturition,Foul Smell of Urine,Bladder Discomfort,Blood in Urine,Lower Back Pain"},
    {"symptoms": "Dizziness,Loss of Balance,Unsteadiness,Weakness of One Body Side,Slurred Speech"},
    {"symptoms": "Irritability,Depression,Lack of Concentration,Altered Sensorium,Mood Swings"},
    {"symptoms": "Itching,Skin Rash,Blisters,Silver Like Dusting,Scurring,Inflammatory Nails"}
]

# Send each test case to API
for i, test in enumerate(test_cases):
    response = requests.post(url, json=test)
    print(f"Test Case {i+1}: {test['symptoms']}")
    print("Prediction:", json.dumps(response.json(), indent=4))
    print("="*50)
